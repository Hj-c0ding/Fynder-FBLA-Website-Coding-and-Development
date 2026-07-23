from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report_item, name='report_item'),
    path('items/', views.found_items, name='found_items'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('items/<int:item_id>/claim/', views.claim_item, name='claim_item'),
    path('moderation/', views.moderation_dashboard, name='moderation_dashboard'),
    path('moderation/item/<int:item_id>/', views.moderate_item, name='moderate_item'),
    path('moderation/claim/<int:claim_id>/', views.moderate_claim, name='moderate_claim'),
]
