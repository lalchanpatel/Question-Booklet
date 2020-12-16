from django.urls import path
from .import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('temp/', views.temp, name='temp'),
    path('signin_page/', views.signin_page, name='signin_page'),
    path('signup_page/', views.signup_page, name='signup_page'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('add_question/', views.add_question, name='add_question'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('dpupdate/', views.dpupdate, name='dpupdate'),
    path('problem/<str:id>/', views.question_view, name='question_view'),
    path('tag/<str:tag_id>/', views.tagsearch, name='tagsearch'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
