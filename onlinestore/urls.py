from django.urls import path

from .import views

urlpatterns = [
    # pages redirections
    path('', views.home, name='home'),
    path('categories/', views.category ,name='categories'),
    path('registration/', views.registration_page, name='register_page'),
    path('loginpage/', views.login_page, name='login_page'),
    path('cart/',views.cart_page,name='cartpage'),
    path('invoice/', views.invoice, name='order_summary'),
    path('success/', views.mail_confirm, name='success'),
    # login functionality
    path('signup/', views.save_data, name='save'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    #login end
    # cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    # path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    # path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
   
]
  
