from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from oscar.apps.address.abstract_models import AbstractUserAddress


class UserAddress(AbstractUserAddress):
    def validate_unique(self, exclude=None):
        super(AbstractUserAddress, self).validate_unique(exclude)
        try:
            self.user
        except:
            return
        qs = self.__class__.objects.filter(
            user=self.user,
            hash=self.generate_hash())
        if self.id:
            qs = qs.exclude(id=self.id)
        if qs.exists():
            raise exceptions.ValidationError({
                '__all__': [_("This address is already in your address"
                              " book")]})


from oscar.apps.address.models import *  # noqa