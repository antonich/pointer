from django.db import IntegrityError


class AlreadyExistsError(IntegrityError):
    pass


class EmptyFieldError(IntegrityError):
    pass
