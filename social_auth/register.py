from django.contrib.auth import authenticate
from users.models import User
from rest_framework.exceptions import AuthenticationFailed
import random
import string
characters = string.ascii_letters + string.punctuation + string.digits
SOCIAL_SECRET = "".join(random.choice(characters) for x in range(random.randint(8, 16)))


def generate_username(name):
    first_name = "".join(name.split(' ')).lower()
    if not User.objects.filter(first_name=first_name).exists():
        return first_name
    else:
        random_username = first_name + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=SOCIAL_SECRET)

            return {
                # 'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'email': email,
            'password': SOCIAL_SECRET}
        user = User.objects.create_user(**user)
        user.auth_provider = provider
        get_name = name.split()
        first_name = str(get_name[0])
        last_name = str(get_name[1])
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        new_user = authenticate(
            email=email, password=SOCIAL_SECRET)
        return {
            'email': new_user.email,
            # 'username': new_user.username,
            'tokens': new_user.tokens()
        }