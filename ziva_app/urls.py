from django.urls import path,include

from ziva_app import views

urlpatterns = [
    path('',views.index,name='index_page'),
    path('store_master',views.store_master,name='store_master'),
    path('add_store',views.add_store,name='add_store'),
    path('item_list',views.item_list,name='item_master'),
    path('item_add',views.item_add,name='item_add'),
    path('category_list',views.category_list,name='category_list'),
    path('category_add',views.category_add,name='category_add'),
    path('region_list',views.region_list,name='region_list'),
    path('region_add',views.region_add,name='region_add'),
    path('warehouse_list',views.warehouse_list,name='warehouse_list'),
    path('warehouse_add',views.warehouse_add,name='warehouse_add'),
]