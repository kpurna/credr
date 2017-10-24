# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Invoice(models.Model):
    invoice_id = models.IntegerField(primary_key=True)
    customer = models.CharField(max_length=20)
    date = models.DateTimeField()
    total_quantity = models.CharField(max_length=20)
    total_amount = models.FloatField(null=True)
    class Meta:
        db_table = 'invoice'

class InvoiceTransactions(models.Model):
    id = models.IntegerField(primary_key=True)
    invoice = models.ForeignKey(Invoice)
    product = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.FloatField(null=True)
    line_total = models.FloatField(null=True)
    class Meta:
        db_table = 'invoice_transactions'

class User(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length=20, blank=True)
    email_id = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'user'

