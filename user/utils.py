from random import choice
from string import ascii_uppercase


from rest_framework.authtoken.models import Token


def get_user_profile(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None

    token = token.split(" ")
    token_obj = Token.objects.filter(key=token[1]).first()

    if not token_obj:
        return None

    if hasattr(token_obj.user, 'userprofile'):
        return token_obj.user.userprofile

    return None


def get_random_hash(length):
    return ''.join(choice(ascii_uppercase) for i in range(length))
