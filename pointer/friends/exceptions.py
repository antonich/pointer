from django.db import IntegrityError


class AlreadyExistsError(IntegrityError):
    pass


class AlreadyFriendsError(IntegrityError):
    pass


class FriendshipNotFoundError(IntegrityError):
    pass
