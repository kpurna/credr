from django.db import models
class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=500)
	email_id=models.CharField(max_length=500)
	status= models.IntegerField(default=0)
	# created_date=models.DateField()()
	class Meta:
	    db_table = 'user'
	    app_label = "credrApp"

class Invoice(models.Model):
	invoice_id = models.AutoField(primary_key=True)
	customer = models.CharField(max_length=500)
	# date=models.DateField()
	total_quantity= models.IntegerField(default=0)
	total_amount=models.IntegerField()
	class Meta:
	    db_table = 'invoice'
	    app_label = "credrApp"

class InvoiceTransactions(models.Model):
	id = models.AutoField(primary_key=True)
	invoice_id = models.IntegerField(max_length=20)
	product = models.CharField(max_length=500)
	quantity=models.CharField(max_length=500)
	price= models.IntegerField(default=0)
	line_total=models.IntegerField()
	class Meta:
	    db_table = 'invoice_transactions'
	    app_label = "credrApp"

