# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
import collections

class AccessoryData(models.Model):
    accessory_id = models.AutoField(primary_key=True) 
    reader_id = models.CharField(max_length=10)
    tag_id = models.CharField(max_length=10)
    access_timestamp = models.DateTimeField(blank=True, null=True)
    accessory_type = models.CharField(max_length=255, blank=True)
    value = JSONField(blank=True,load_kwargs={'object_pairs_hook': collections.OrderedDict}) 
    class Meta:
        managed = False
        db_table = 'accessory_data'

class ReaderLocation(models.Model):
    reader = models.ForeignKey('Readers')
    location_id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    start_timestamp = models.DateTimeField(blank=True, null=True)
    end_timestamp = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'reader_location'

class Readers(models.Model):
    reader_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    user_id = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'readers'

class TagAnimal(models.Model):
    animal_id = models.AutoField(primary_key=True) 
    tag = models.ForeignKey('Tags')
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=500, blank=True)
    start_timestamp = models.DateTimeField(blank=True, null=True)
    end_timestamp = models.DateTimeField(blank=True, null=True)
    field_data = JSONField(blank=True,load_kwargs={'object_pairs_hook': collections.OrderedDict})
    class Meta:
        managed = False
        db_table = 'tag_animal'

class TagReads(models.Model):
    tag_reads_id = models.AutoField(primary_key=True)
    reader = models.ForeignKey(Readers)
    tag = models.ForeignKey('Tags')
    tag_timestamp = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'tag_reads'

class Tags(models.Model):
    tag_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=500, blank=True)
    user_id = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tags'

