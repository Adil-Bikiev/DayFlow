from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DayFlowApp.urls')),
]

if settings.DEBUG is False:
    urlpatterns += [
        path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    ]

handler404 = 'DayFlowApp.views.custom_page_not_found_view'