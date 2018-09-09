from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.sites.models import Site

from tenant_schemas.models import TenantMixin


def create_site(sender, instance, created, **kwargs):
    s = Site.objects.get_or_create(domain=instance.domain_url,
    name=instance.domain_url)


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return F'{self.schema_name} - {self.domain_url}'

    def update(self, *args, **kwargs):
        print(vars(self))
        super().update(*args, **kwargs)

post_save.connect(create_site, sender=Client)
