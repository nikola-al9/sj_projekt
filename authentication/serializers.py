from django.contrib.auth import password_validation
from rest_framework import serializers
from authentication.models import Account


class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Account
        fields = ['id',
                  'name',
                  'email',
                  ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        if Account.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email', 'Email is already taken'})
        return super().validate(attrs)


class UpdateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'name',
            'email',
        ]


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'email',
            'password'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        print(user)
        if not user.check_password(value):
            raise serializers.ValidationError(
                'Your old password was entered incorrectly. Please enter it again.'
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': "The two password fields didn't match."})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class ListAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'email',
            'is_admin',
            'is_staff'
        )
