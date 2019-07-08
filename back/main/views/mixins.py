from rest_framework.exceptions import PermissionDenied, NotFound
from main.models import User


class ParseObjectOwnerMixin(object):
    """
    Converts user_id into self.user object.
    """
    user_lookup_url_kwarg = 'user_id'
    obj_user = None

    def initial(self, request, *args, **kwargs):
        try:
            user_id = int(self.kwargs.pop(self.user_lookup_url_kwarg))
            assert 0 < user_id < 10 ** 8
            self.obj_user = User.objects.get(id=user_id)
        except (ValueError, TypeError, AssertionError, User.DoesNotExist):
            self.obj_user = None

        super(ParseObjectOwnerMixin, self).initial(request, *args, **kwargs)

        if self.obj_user is None:
            raise NotFound

        if self.obj_user != request.user:
            raise PermissionDenied
