"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from miapp import views
from miapp.views import book_list, book_create, book_update, book_delete, review_create, review_delete


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login'), name='home'),  # Redirige a login inicialmente
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),  # La página home a la que se redirige tras login exitoso
    path('user/list/', views.user_list, name='user_list'),
    path('user/edit/', views.user_edit, name='user_edit'),
    path('user/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('user/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('register/', views.register_view, name='register'),
    path('libros/', book_list, name='book_list'),
    path('libros/crear/', book_create, name='book_create'),
    path('libros/<int:book_id>/editar/', book_update, name='book_update'),
    path('libros/<int:book_id>/eliminar/', book_delete, name='book_delete'),
    path('libros/<int:book_id>/reseña/', review_create, name='review_create'),
    path('reseña/<int:review_id>/eliminar/', review_delete, name='review_delete'),
]


