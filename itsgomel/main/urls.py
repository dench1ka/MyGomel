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
    path('before_after/', views.before_after_list, name='before_after_list'),
    path('before_after/<int:pk>/', views.before_after_detail, name='before_after_detail'),
    path('college/', views.college_list, name='college_list'),
    path('college/college_events/', views.college_events, name='college_events'),
    path('college/dorm_events/', views.dorm_events, name='dorm_events'),
    path('college/cultural_events/', views.cultural_events, name='cultural_events'),
    path('college/<int:pk>/', views.college_detail, name='college_detail'),
    path('history/', views.history_list, name='history_list'),
    path('history/<int:pk>/', views.history_detail, name='history_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
