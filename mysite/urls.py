from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # ui
    path(r'jet/', include('jet.urls', 'jet')),
    
    path('admin/', admin.site.urls),
    # path('', admin.site.urls),
    path('api/accounts/', include('accounts.api.urls', 'accounts_api')),
    path('api/products/', include('products.api.urls', 'products_api')),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
