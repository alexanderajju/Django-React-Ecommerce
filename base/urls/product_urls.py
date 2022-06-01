from django.urls import path
from base.views import product_view as views

urlpatterns = [

    path('', views.getProducts, name='products'),


    path('create/', views.createProduct, name='create_product'),
    path('upload/', views.uploadImage, name='image'),

    path('<str:pk>/reviews/', views.createProductReview, name='product_review'),
    
    path('top/', views.getTopProducts, name='ptop_roduct'),
    path('<str:pk>/', views.getProduct, name='product'),
    
    path('update/<str:pk>/', views.updateProduct, name='update_product'),
    path('delete/<str:pk>/', views.deleteProduct, name='delete_product'),
]
