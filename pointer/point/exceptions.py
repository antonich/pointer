from django.db import IntegrityError


class AlreadyExistsError(IntegrityError):
    pass


class PointerIsOutOfDateError(IntegrityError):
    pass


class EmptyFieldError(IntegrityError):
    pass

class MemberDoesnotExists(IntegrityError):
    pass
#
#
# class RequestNotFoundError(IntegrityError):
#     pass
