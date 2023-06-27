from django.urls import path

from users import views

urlpatterns = [
    path('', views.ProfileListAPIView.as_view()),
    path('<str:pk>/', views.ProfileRetrieveUpdateAPIView.as_view()),
]
