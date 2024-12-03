from django.urls import path

from accounts.api.views import(
    registration_view,

)
from rest_framework.authtoken.views import obtain_auth_token

app_name = "accounts"


urlpatterns = [
        path('signup', registration_view, name="register"),
      
]