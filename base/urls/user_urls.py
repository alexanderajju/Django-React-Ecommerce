from django.urls import path
from base.views import user_view as views


urlpatterns = [

    path('', views.getUsers, name='users'),
    path('register/', views.registerUser, name='register'),
    path('profile/', views.getUserProfile, name='user_profile'),
    path('profile/update/', views.updateUserProfile, name='user_profile_update'),
    path('login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('<str:pk>/', views.getUsersById,name='user-admin-call'),

    path('update/<str:pk>/', views.updateUserProfileByAdmin,name='update_UserProfileByAdmin'),
    
    path('delete/<str:pk>/', views.deleteUser,name='deletUser')
]
