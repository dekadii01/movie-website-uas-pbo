from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserService:

  @staticmethod
  def update_user(user_id, data):
        user = User.objects.get(id=user_id)

        user.username = data.get("username")
        user.email = data.get("email")
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")

        user.is_staff = data.get("is_staff") == "on"
        user.is_active = data.get("is_active") == "on"

        user.save()
        return user

  @staticmethod
  def delete_user(user_id):
        user = User.objects.get(id=user_id)
        user.delete()
  