from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
   path('',views.index,name='index'),
   path('new/profile',views.new_profile, name='profile'),
   path('search/', views.search_results, name='search_results'),
   path('logout', views.logout, name='logout'),
   path('project/', views.project,name='project'),
   path('rating/<int:pk/', views.rating,name='rating'),
  
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)