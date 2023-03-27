class UserMixin:
    """Mixin for user model."""

    def get_deleted_user(self):
        deleted_user = self.objects.get_or_create(username="deleted")[0]
        if deleted_user.is_active is not False:
            deleted_user.is_active = False
            deleted_user.save()
        return deleted_user
