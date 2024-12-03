from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter 
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime, timedelta
from collections import defaultdict
from rest_framework.permissions import  IsAuthenticated
import threading
import re
from django.shortcuts import get_object_or_404
from accounts.models import (
    Account,
    )
from products.models import (
    ProductDetails,
    )

from products.api.serializers import (
    ProductSerializer,
)
from rest_framework.authtoken.models import Token


class ProductListView(ListAPIView):
    # queryset = ProductDetails.objects.all()
    queryset = ProductDetails.objects.prefetch_related('images', 'category', 'sub_category')
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    

