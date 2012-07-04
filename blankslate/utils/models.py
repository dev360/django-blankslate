import uuid 

from django.core import serializers
from django.contrib.gis.db import models
from django.utils import simplejson


class GUIDModel(models.Model):
    """ A base model that uses GUIDs instead of 
    auto-incrementing integers. """
    
    id = models.CharField(primary_key=True, max_length=40, editable=False)

    def ensure_id(self):
        if not self.id:
            self.id = str(uuid.uuid1())

    def save(self, *args, **kwargs):
        """ Overrides the save and generates the guid, generated from
        host id, seq and time. """
        self.ensure_id()
        super(GUIDModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
