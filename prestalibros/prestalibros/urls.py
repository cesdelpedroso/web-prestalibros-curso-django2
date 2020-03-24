"""prestalibros URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import include,url
from django.contrib import admin
from django.urls import path


from django.conf import settings
from django.conf.urls.static import static

from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indice, name='indice'),

    path('books/', views.BookListView, name='books'),
    path('book/<int:pk>', views.BookDetailView, name='book-detail'),
    path('book/create/', views.BookCreate, name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate, name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete, name='book_delete'),

    path('usuario/<int:pk>/delete/', views.UsuarioDelete, name='usuario_delete'),
    path('usuario/create/', views.UsuarioCreate, name='usuario_create'),
    path('usuario<int:pk>/update/', views.UsuarioUpdate, name='usuario_update'),
    path('usuario/<int:pk>', views.UsuarioDetail, name='usuario_detail'),
    path('usuario/', views.UsuarioList, name='usuario_list'),
    path('usuario/book_list', views.Usuario_BookListView, name='book_usuario'),
    path('book/<int:pk>/request_issue/', views.usuario_request_issue, name='request_issue'),

    
    path('return/<int:pk>', views.ret, name='ret'),
    path('rating/<int:pk>/update/', views.RatingUpdate, name='rating_update'),
    path('rating/<int:pk>/delete/', views.RatingDelete, name='rating_delete'),


url(r'^search_b/', views.search_book, name="search_b"),
url(r'^search_u/', views.search_user, name="search_u")
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)