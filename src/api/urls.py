from django.urls import path

from api import views

urlpatterns = [
    path('users/', views.ProfileListAPIView.as_view()),
    path('users/<str:pk>/', views.ProfileRetrieveUpdateAPIView.as_view()),
    path('product-category/', views.ProductCategoryListAPIView.as_view()),
    path('products/', views.ProductListAPIView.as_view()),
]
