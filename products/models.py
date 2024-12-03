from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.text import slugify
import os
from uuid import uuid4
from PIL import Image, ImageDraw, ImageFont


def upload_location(instance, filename):
    # Ensures unique filenames by appending a UUID
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('products', filename)



def add_watermark(image_path, watermark_text="Watermark"):
    # Open the original image
    image = Image.open(image_path).convert("RGBA")

    # Make a blank image for the watermark with an alpha layer
    watermark = Image.new("RGBA", image.size, (255, 255, 255, 0))

    # Get a drawing context
    draw = ImageDraw.Draw(watermark)

    # Define the font path and load the font
    font_path = "fonts/Lato-Regular.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found at {font_path}")
    font = ImageFont.truetype(font_path, 30)

    # Get the text bounding box and calculate its size
    text = watermark_text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Position the text in the bottom-right corner
    position = (image.size[0] - text_width - 10, image.size[1] - text_height - 10)
    
    # Draw the text onto the watermark image
    draw.text(position, text, fill=(255, 255, 255, 128), font=font)

    # Combine the original image with the watermark
    watermarked_image = Image.alpha_composite(image, watermark)

    # Determine the format of the original image
    original_format = image.format

    # Save the result back to the original file, preserving the format
    if original_format == "PNG":
        watermarked_image.save(image_path, format="PNG")
    elif original_format == "WEBP":
        # WEBP-specific handling: ensure it supports transparency
        watermarked_image.save(image_path, format="WEBP", lossless=True)  # Use lossless if desired
    else:
        # Default to JPEG for other formats, removing alpha transparency
        watermarked_image = watermarked_image.convert("RGB")  # Drop alpha for JPEG
        watermarked_image.save(image_path, format="JPEG")



class Category(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Category Name")

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Sub-Category Name")

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class ProductDetails(models.Model):
    name                =    models.CharField(max_length=50, null=False, blank=False, verbose_name="Product Name")
    description         =    models.TextField(null=False, blank=False, verbose_name="Description")
    creator             =    models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Created By")
    price               =    models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Price")
    product_image       =    models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name="Product Image")
    category            =    models.ManyToManyField(Category, related_name='products', verbose_name="Categories")
    sub_category        =    models.ManyToManyField(SubCategory, related_name='products', verbose_name="Sub-Categories")
    slug 	    		=    models.SlugField(blank=False, unique=True)



    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['creator']),
            models.Index(fields=['price']),
            # models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE, related_name='images', verbose_name="Product")
    
    image = models.ImageField(upload_to=upload_location, verbose_name="Image")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Add watermark after the file is saved
        add_watermark(self.image.path, watermark_text="E-com")

    def __str__(self):
        return f"Image for {self.product.name if self.product else 'No product assigned'}"


@receiver(post_delete, sender=ProductImage)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


def Product_slug_gen(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(str(instance.creator)+ "-" + instance.name)

pre_save.connect(Product_slug_gen, sender=ProductDetails)