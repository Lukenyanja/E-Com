from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import  IsAuthenticated
from django.contrib.auth import authenticate, login
from accounts.models import (
    Account,
    )

from accounts.api.serializers import (
    RegistrationSerializer,
)
from rest_framework.authtoken.models import Token

@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            accounts = serializer.save()
            data['response'] = "sucessfuly registered"
            data['password'] = accounts.password
            token = Token.objects.get(user=accounts).key
            data['token'] = token
            # data['phone_number'] = accounts.phone_number
  
        else:
            data = serializer.errors
        
        return Response(data)
