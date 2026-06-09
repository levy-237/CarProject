from django.contrib.auth.hashers import make_password, check_password


def hash_code(code):
    return make_password(str(code))


def verify_code(raw_code, hashed_code):
    return check_password(str(raw_code), hashed_code)