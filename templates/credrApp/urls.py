from django.conf.urls import patterns, include, url
from django.conf.urls import *
from tastypie.api import Api
from credrApp.views import user_details,index
from credrApp.api.user import InvoiceResource,InvoiceTransactionsResource

v1_api = Api(api_name='v1')
# v1_api.register(UserResource())
v1_api.register(InvoiceResource())
v1_api.register(InvoiceTransactionsResource())


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', index.index),
	(r'^admin/', include(admin.site.urls)),
	(r'', include(v1_api.urls)),
	# url(r'^v0/user-details/$',user_details.user_details),
	url(r'^v0/invoice-details/$',user_details.invoice_details),
	url(r'^v2/invoice-details/(\d+)/$',user_details.invoice_details_with_id),
)
