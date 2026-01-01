from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class AuthService:

    @staticmethod
    def register_user(full_name, email, password, password2):
        if password != password2:
            raise ValidationError("Password tidak cocok")

        if User.objects.filter(username=email).exists():
            raise ValidationError("Email sudah terdaftar")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name,
            is_staff=False,
            is_superuser=False
        )

        user.save()
        return user


    @staticmethod
    def login_user(email, password):
        user = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError("Email atau password salah")

        return user
