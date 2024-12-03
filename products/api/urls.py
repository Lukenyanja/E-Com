from django.urls import path

from products.api.views import(
    ProductListView,

)
from rest_framework.authtoken.views import obtain_auth_token

app_name = "products"


urlpatterns = [
        path('products/', ProductListView.as_view(), name="products"),
      
]