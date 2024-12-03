from rest_framework import serializers
from django.conf import settings
from urllib.parse import urljoin



from accounts.models import (
    Account,
    )

from products.models import (
    ProductDetails,
    )

class ProductSerializer(serializers.ModelSerializer):
    creator                 = serializers.StringRelatedField()
    category                = serializers.StringRelatedField(many=True)
    sub_category            = serializers.StringRelatedField(many=True)
    images                  = serializers.SerializerMethodField()


    class Meta:
        model = ProductDetails

        fields = ['name', 'description', 'creator','price','category','sub_category','images' 
                  
                  ]
        
    def get_images(self, obj):
        request = self.context.get('request')
        if request:
            # Use the request object to build absolute URLs
            return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
        else:
            # Fallback to manually constructing URLs if request is not available
            return [urljoin(settings.MEDIA_URL, image.image.url) for image in obj.images.all()]

    def get_category(self, obj):
        return [category.name for category in obj.category.all()]
    def get_sub_category(self, obj):
        return [sub_category.name for sub_category in obj.sub_category.all()]

