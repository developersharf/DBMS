from django.urls import path
from .views import submit_found_item, list_found_items, found_detail
from . import views

urlpatterns = [
    path('submit/', submit_found_item, name='submit_found'),
    path('list/', list_found_items, name='list_found'),
    path('<int:id>/', found_detail, name='found_detail'),
    path('my-items/', views.user_found_items_view, name='user_found_items'),
    path('edit/<int:id>/', views.edit_found_item, name='edit_found_item'),
    path('delete/<int:id>/', views.delete_found_item, name='delete_found_item'),
]
