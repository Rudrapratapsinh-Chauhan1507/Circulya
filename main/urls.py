from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    path('', views.feed_view, name='feed'),
    path('add-product/', views.add_product_view, name='add_product'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('purchases/', views.view_purchases, name='purchases'),
]
