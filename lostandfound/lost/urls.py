from django.urls import path
from . import views
from .views import list_lost_items, submit_lost_item, match_found_items

urlpatterns = [
    path('submit-lost/', submit_lost_item, name='submit_lost'),
    path('', list_lost_items, name='list_lost'),
    path('list_confidence/', match_found_items, name='list_confidence'),
    path('list_confidence/<int:lost_id>/', views.match_found_items, name='list_confidence'),
    path('<int:id>/', views.lost_detail, name='lost_detail'),
    path('user-items/', views.user_lost_items, name='user_lost_items'),
    path('edit/<int:id>/', views.edit_lost_item, name='edit_lost_item'),
    path('delete/<int:id>/', views.delete_lost_item, name='delete_lost_item'),
]
