from django.urls import path

from api import views

urlpatterns = [
    path('users/', views.ProfileListAPIView.as_view()),
    path('users/<str:pk>/', views.ProfileRetrieveUpdateAPIView.as_view()),
    path('users/<str:pk>/rents/', views.ProfileRentListAPIView.as_view()),
    path('product-categories/', views.ProductCategoryListAPIView.as_view()),
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/<str:pk>/', views.ProductRetrieveUpdateAPIView.as_view()),
    path('reviews/', views.ProductReviewsListCreateAPIView.as_view()),  # TODOOO: fix and test
    path('rents/', views.RentCreateAPIView.as_view()),
]


"""
TODOOOOOOO:

- [GET, PATCH] /products/<str:pk>/ (only owner of product can update)
    visualizzazione e aggiornamento prodotto (si può copiare dal servizio users/<str:pk>/)

- [GET, POST] /products/<str:pk>/images/ (only owner of product can create)
    visualizzazione e caricamento immagini del prodotto
- [DELETE] /products/<str:pk>/images/<str:pk>/ (only owner of product can delete)
    cancellazione immagine del prodotto a db (come viene cancellata l'immagine dal server?)

- [POST] /rents/
    -> (Alex) poi mandare notifica con Firebase Cloud Messaging all'owner del prodotto che deve accettare o rifiutare

- [GET] /products/products/rents/ (only owner of PRODUCT can view) [product__owner]
    owner può vedere i noleggi del suo prodotto


- creare modello Business
- servizio per approvare o rifiutare noleggio (solo owner del prodotto)
- servizio per cancellare il noleggio (solo owner del rent)
- rivedere servizio reviews (solo chi ha noleggiato il prodotto può lasciare una recensione)
"""
