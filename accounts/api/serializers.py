from rest_framework import serializers
from django.conf import settings
from urllib.parse import urljoin



from accounts.models import (
    Account,
    )

class RegistrationSerializer(serializers.ModelSerializer):


    class Meta:
        model = Account
        fields = ['email', 'username','password'
                    ]
        extra_kwargs = { 
                    'password': {'write_only' : True}
        }

    def save(self):
        accounts = Account(
                    email                       =self.validated_data['email'],
                    username                    =self.validated_data['username'],

                    

        )
        password = self.validated_data['password']

        accounts.set_password(password)
        accounts.save()
        return accounts