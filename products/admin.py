from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from products.models import (
    ProductDetails,
    Category,
    SubCategory,
    ProductImage,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius:7px;" />', 
                obj.image.url
            )
        return "No Image"



class ProductAdminForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.FileInput(attrs={'allow_multiple_selected': True}),  # Correct widget for multiple file uploads
        required=False,
        label="Upload Images",
    )

    class Meta:
        model = ProductDetails
        fields = ['name', 'description','price','creator','category','sub_category','slug']  # Add any other fields from your `ProductDetails` model


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [ProductImageInline]
    list_display = ['id', 'name']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Handle multiple image uploads
        images = request.FILES.getlist('images')  # Fetch list of uploaded files
        for image in images:
            ProductImage.objects.create(product=obj, image=image)
 

admin.site.register(ProductDetails, ProductAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ProductImage)
