from django.contrib import admin

from api.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lastname', 'type', 'is_verified', 'is_active', 'sign_in_provider')
    readonly_fields = ('id', 'user', 'sign_in_provider', 'created_at', 'updated_at')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    readonly_fields = ('id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'owner', 'active', 'stock_quantity')
    readonly_fields = ('id', 'owner', 'created_at', 'updated_at')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')
    readonly_fields = ('id',)


@admin.register(ProductReviews)
class ProductReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'owner', 'rating')
    readonly_fields = ('id', 'product', 'owner', 'created_at')


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'renter', 'status', 'start_time', 'end_time')
    readonly_fields = ('id', 'product', 'renter', 'created_at', 'updated_at')
