from django.urls import path, include

import users.urls

urlpatterns = [
    path('users/', include(users.urls)),
]
