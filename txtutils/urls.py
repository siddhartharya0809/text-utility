from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('removepunc', views.removepunc, name='removepunc'),
    path('about', views.about, name='about'),
    
    # NEW: File Utility URL
    path('file-utility/', views.file_utility, name='file_utility'),
]