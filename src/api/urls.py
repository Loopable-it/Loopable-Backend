from django.urls import path

from api import views

urlpatterns = [
    path('users/', views.ProfileListAPIView.as_view()),
    path('users/<str:pk>/', views.ProfileRetrieveUpdateAPIView.as_view()),
    path('product-categories/', views.ProductCategoryListAPIView.as_view()),
    path('products/', views.ProductListAPIView.as_view()),
    path('reviews/', views.ProductReviewsListCreateAPIView.as_view()),
    path('rents/', views.RentListCreateAPIView.as_view()),
]


"""
TODOOOOOOO:
- creare modello Business
- serializzare errore 404, 500 come json

- [GET, PATCH] /products/<str:pk>/ (only owner of product can update)
    visualizzazione e aggiornamento prodotto (si può copiare dal servizio users/<str:pk>/)

- [GET, POST] /products/<str:pk>/images/ (only owner of product can create)
    visualizzazione e caricamento immagini del prodotto
- [DELETE] /products/<str:pk>/images/<str:pk>/ (only owner of product can delete)
    cancellazione immagine del prodotto a db (come viene cancellata l'immagine dal server?)

- [GET, POST] /rents/ (da creare i filtri product__owner=uid, renter=uid - deve essere sicuro) + TEST 
    visualizzazione + creazione noleggio -> da forzare stato creazione a "pending" 
        -> (Alex) poi mandare notifica con Firebase Cloud Messaging all'owner del prodotto che deve accettare o rifiutare
- [GET] /users/<str:pk>/rents/ (only owner can view)
    visualizzazione dei prodotti di cui ho fatto richiesta di noleggio (renter=user_pk)

- [GET] /products/<str:pk>/rents/ (only owner of product can view)
    owner può vedere i noleggi del suo prodotto


- servizio per approvare o rifiutare noleggio (solo owner del prodotto)
- servizio per cancellare il noleggio (solo owner del rent)
- rivedere servizio reviews (solo chi ha noleggiato il prodotto può lasciare una recensione)
"""
