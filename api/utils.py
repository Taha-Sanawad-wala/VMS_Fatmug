from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


def create_token_for_user(username):
    user=User.objects.get(username=username)
    token,created=Token.objects.get_or_create(user=user)
    return token
