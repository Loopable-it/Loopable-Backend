"""
URL configuration for loopable project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from loopable.views import PingPongView, custom404, custom500

SchemaViewSwagger = get_schema_view(
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
    path('api/v1/', include('api.urls', namespace='v1')),
]

if settings.DEBUG or settings.SWAGGER_ALLOWED:  # Static only if allowed
    urlpatterns.append(
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    )
