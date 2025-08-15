from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='home'),
    # path('mural', views.mural, name='murali')
    path('murals/', views.mural, name='murals'),
    path('murals/<int:pk>/', views.mural_detail, name='mural_detail'),
    path('suggest_mural/', views.suggest_mural, name='suggest_mural'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
