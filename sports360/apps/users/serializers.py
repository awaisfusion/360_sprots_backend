from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.users.models import User, EmailVerification


class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'role', 'role_display',
                  'phone', 'is_verified', 'email_verified_at', 'business_name', 'business_description')
        read_only_fields = ('id', 'role_display', 'email_verified_at')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=['customer', 'business'], default='customer')

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'role', 'first_name',
                  'last_name', 'phone', 'business_name', 'business_description',
                  'business_registration_number')

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match'})

        # Validate business fields if registering as business
        if data.get('role') == 'business':
            if not data.get('business_name'):
                raise serializers.ValidationError({'business_name': 'Business name is required for business accounts'})
            if not data.get('business_registration_number'):
                raise serializers.ValidationError({'business_registration_number': 'Business registration number is required'})

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            role=validated_data.get('role', 'customer'),
            business_name=validated_data.get('business_name', ''),
            business_description=validated_data.get('business_description', ''),
            business_registration_number=validated_data.get('business_registration_number', ''),
            is_verified=False,
        )
        return user


class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name', 'phone')

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            role='admin',
            is_verified=True,  # Admins don't need email verification
            is_active=True,
        )
        return user


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role
        token['is_verified'] = user.is_verified
        token['is_business'] = user.is_business()
        token['is_admin'] = user.is_admin()
        return token


class SendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.is_verified:
                raise serializers.ValidationError("Email already verified")
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        return value


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)

    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Code must be 6 digits")
        return value

