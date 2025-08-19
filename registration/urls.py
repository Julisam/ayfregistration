from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('id-card/<int:pk>/', views.id_card, name='id_card'),
    path('bulk-print/', views.bulk_print, name='bulk_print'),
]