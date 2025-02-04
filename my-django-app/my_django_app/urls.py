from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('secured/', views.secured_view, name='secured'),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
]