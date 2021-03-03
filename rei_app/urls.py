from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('my_account', views.my_account),
    path('rental_type', views.rental_type),
    path('rental_parse', views.rental_parse),
    path('broad_search', views.broad),
    path('search_properties', views.search_properties),
    path('create_lead', views.create_lead),
    path('remove_lead/<int:num>', views.remove_lead),
    path('investment_performance/<str:state>/<str:city>', views.investment_performance),
]