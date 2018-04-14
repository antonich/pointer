from django.db import IntegrityError


class MemberAlreadyExistsError(IntegrityError):
    pass

class EmptyFieldError(IntegrityError):
    pass

class MemberDoesnotExists(IntegrityError):
    pass
