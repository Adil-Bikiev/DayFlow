from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DayFlowApp.urls')),
]

handler404 = 'DayFlowApp.views.custom_page_not_found_view'