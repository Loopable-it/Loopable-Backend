"""
URL configuration for loopable project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from loopable.views import PingPongView, custom404, custom500

schema_view = get_schema_view(
    openapi.Info(
        title='Loopable API',
        default_version='v1',
        description='Loopable Django API',
        terms_of_service='https://loopable.it',
        contact=openapi.Contact(email='contact@loopable.it'),
    ),
    public=True,
    permission_classes=(),  # noqa
    authentication_classes=()  # noqa
)

if not settings.DEBUG:
    handler404 = custom404
    handler500 = custom500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stats/ping/', PingPongView.as_view()),
    path('stats/ht/', include('health_check.urls')),
    path('api/v1/', include('api.urls')),
]

if settings.DEBUG or settings.SWAGGER_ALLOWED:  # Swagger only if allowed
    urlpatterns.append(
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    )
    urlpatterns.append(
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    )
    urlpatterns.append(
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    )
