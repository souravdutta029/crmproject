from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user-page'),
    path('account/', views.accountSettings, name='account'),

    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('create-order/<str:pk>/', views.createOrder, name='create-order'),
    path('update-order/<str:pk>/', views.updateOrder, name='update-order'),
    path('delete-order/<str:pk>/', views.deleteOrder, name='delete-order'),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.htm'), name='reset_password'),
    
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.htm'), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.htm'), name='password_reset_confirm'),
    
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.htm'), name='password_reset_complete'),
]