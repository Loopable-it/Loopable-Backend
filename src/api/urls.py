from django.conf import settings
from django.urls import path, re_path

from api import views
from loopable.urls import SchemaViewSwagger

app_name = 'api_v1'

urlpatterns = [
    path('users/', views.ProfileListAPIView.as_view()),
    path('users/<str:pk>/', views.ProfileRetrieveUpdateAPIView.as_view()),
    path('users/<str:pk>/rents/', views.ProfileRentListAPIView.as_view()),  # user is the render
    path('users/<str:pk>/reviews/', views.ProfileReviewsListAPIView.as_view()),
    path('users/<str:pk>/products/rents/', views.ProfileProductRentListAPIView.as_view()),  # user is the owner
    path('product-categories/', views.ProductCategoryListAPIView.as_view()),
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/<str:pk>/', views.ProductRetrieveUpdateAPIView.as_view()),
    path('products/<str:pk>/reviews/', views.ProductReviewsListAPIView.as_view()),
    path('products/<str:pk>/images/', views.ProductImageCreateAPIView.as_view()),
    path('products/<str:pk>/images/<str:id_img>/', views.ProductImageDestroyAPIView.as_view()),
    path('reviews/', views.ProductReviewsCreateAPIView.as_view()),
    path('rents/', views.RentCreateAPIView.as_view()),
    path('rents/<str:pk>/', views.RentUpdateAPIView.as_view()),
]


"""
TODOOOOOOO:

- [POST] /rents/ -> email
    -> (Alex) poi mandare notifica con Firebase Cloud Messaging all'owner del prodotto che deve accettare o rifiutare

- [GET] /users/<id>/products/rents/ (only owner of PRODUCT can view) [product__owner]  # user is the owner
    owner può vedere i noleggi del suo prodotto

- creare modello Business
"""

if settings.DEBUG or settings.SWAGGER_ALLOWED:  # Docs only if allowed
    urlpatterns.append(
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', SchemaViewSwagger.without_ui(cache_timeout=0), name='schema-j'),
    )
    urlpatterns.append(
        re_path(r'^swagger/$', SchemaViewSwagger.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    )
    urlpatterns.append(
        re_path(r'^redoc/$', SchemaViewSwagger.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    )
