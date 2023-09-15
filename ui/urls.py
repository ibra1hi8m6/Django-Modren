from django.urls import path
from . import views

urlpatterns = [
    path("signup/",views.signup),
    path('', views.index),
    path('auth/', views.auth),
    path('cart/', views.cart),
    path('category/<int:id>/', views.category),
    path('checkout/', views.checkout),
    path('login/', views.loginPage),
    path('login/<int:displayErrorMessage>/', views.loginPage),
    path('products/', views.products),
    path('newuser/', views.createuser)
]
