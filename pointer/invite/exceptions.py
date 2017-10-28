from django.db import IntegrityError


class InviteAlreadyExistsError(IntegrityError):
    pass


class EmptyFieldError(IntegrityError):
    pass

class InviteOnlyFriendsError(IntegrityError):
    pass

class AlreadyMemberOfThisPointer(IntegrityError):
    pass
