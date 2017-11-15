from django.db import IntegrityError

class NoTokenForUser(IntegrityError):
    pass

class UserAlreadyInUse(IntegrityError):
    pass
