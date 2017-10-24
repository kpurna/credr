from tastypie.resources import ModelResource
from credrApp.models.user import Invoice, InvoiceTransactions
from tastypie.authorization import Authorization

# class UserResource(ModelResource):
# 	class Meta:
# 		collection_name="data"
# 		queryset = User.objects.all()
#  		resource_name = 'user'
# 		authorization = Authorization()
# # 		excludes = ['last_login','id']
# #   		fields=["email_id","name"]
# # 		list_allowed_methods = ["post","get","put","patch"]        
# # 		detail_allowed_methods = ["get","put","patch","delete"]

class InvoiceResource(ModelResource):
	class Meta:
		collection_name = "data"
		queryset = Invoice.objects.all()
		resource_name = 'invoice'
		authorization = Authorization()

class InvoiceTransactionsResource(ModelResource):
	class Meta:
		collection_name = "data"
		queryset = InvoiceTransactions.objects.all()
		resource_name = 'invoice_transactions'
		authorization = Authorization()	