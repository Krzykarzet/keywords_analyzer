from django.urls import path

from . import views

app_name = 'ka'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('cresults/', views.cresults, name='cresults'),
]