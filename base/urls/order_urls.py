from django.urls import path
from base.views import order_view as views

urlpatterns = [
     path('', views.getOrders, name='Orders'),
    path('add/', views.addOrderItems, name='add_order'),
   
    path('myorders/', views.getMyOrders, name='myOrders'),

     path('<str:pk>/deliver/', views.updateOrderToDelivered, name='order_deliver'),

    path('<str:pk>/', views.getOrderById, name='user_order'),
    path('<str:pk>/pay/', views.updateOrderToPaid, name='user_orderPay'),

]
