from django.db import IntegrityError


class InviteAlreadyExistsError(IntegrityError):
    pass


class EmptyFieldError(IntegrityError):
    pass
