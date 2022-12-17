from django.urls import path,include

from ziva_app import views

urlpatterns = [
    path('',views.index,name='index_page'),
    path('store_master',views.store_master,name='store_master'),
    path('add_store',views.add_store,name='add_store'),
    path('item_master',views.item_master,name='item_master'),
    path('item_add',views.item_add,name='item_add'),
    path('category_master',views.category_master,name='category_master'),
    path('category_add',views.category_add,name='category_add')
]