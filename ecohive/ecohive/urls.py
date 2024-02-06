"""
URL configuration for ecohive project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from ecohiveapp import views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from ecohiveapp.views import CustomGoogleLoginView

urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.index, name='index'),

    path('register.html', views.register, name='register'),
    # path('seller_register.html', views.seller_register, name='seller_register'),
    path('login.html', views.user_login, name='login'),
    path('dashlegal.html', views.dashlegal, name='dashlegal'),
    path('dashseller.html', views.dashseller, name='dashseller'),
    path('successseller.html', views.successseller, name='successseller'),
    path('successaddcategory.html', views.successaddcategory, name='successaddcategory'),
    path('successaddproduct.html', views.successaddproduct, name='successaddproduct'),
    path('admindash', views.admindash, name='admindash'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('viewcategory', views.viewcategory, name='viewcategory'),
    path('sellerorder', views.sellerorder, name='sellerorder'),


    path('viewaddproduct', views.viewaddproduct, name='viewaddproduct'),
    path('addproducts', views.addproducts, name='addproducts'),
    path('viewproducts', views.viewproducts, name='viewproducts'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),

    path('approve_certification/<int:certification_id>/', views.approve_certification, name='approve_certification'),
    path('reject_certification/<int:certification_id>/', views.reject_certification, name='reject_certification'), 

    path('delete_add_product/<int:product_id>/', views.delete_add_product, name='delete_add_product'),
    path('logout/', views.loggout, name='loggout'),
    path('check_email/', views.check_email, name='check_email'),
    path('check_username/', views.check_username, name='check_username'),
    # Include allauth URLs for other authentication-related views
    path('accounts/', include('allauth.urls')),
    # Include allauth.socialaccount URLs
    path('accounts/', include('allauth.socialaccount.urls')),
    # path('select-user-type/', views.select_user_type, name='select_user_type'),
    # path('google-login/', views.google_login, name='google_login'),
    # path('google-login/', CustomGoogleLoginView.as_view(), name='custom_google_login'),
   # Define the URL for approving an application
    # path('approve_application/<int:application_id>/', views.approve_application, name='approve_application'),
    # # Define the URL for rejecting an application
    # path('reject_application/<int:application_id>/', views.reject_application, name='reject_application'),
    # path("accounts/", include("allauth.urls")),
    #USER DASHBOARD
    path('profile', views.profile, name='profile'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user_list', views.user_list, name='user_list'),
    path('toggle_user_status/<int:user_id>/', views.user_status_toggle, name='user_status_toggle'),



    path('viewstock', views.view_products, name='viewstock'),
    path('product-summary/<int:pk>/edit/', views.edit_product_stock, name='edit_product_stock'),


    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    #customerpages
    path('wishlist', views.wishlist, name='wishlist'),
    path('product/<int:product_id>/', views.product_single, name='product_single'),
    path('checkout', views.checkout, name='checkout'),
    path('cart/', views.cart_view, name='cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('payment', views.payment, name='payment'),
    path('orders/', views.orders, name='orders'),
    path('view_orders', views.view_orders, name='view_orders'),
    path('generate_pdf/<int:order_id>/', views.generate_pdf, name='generate_pdf'),


    # path('wishlist/', views.wishlist_view, name='wishlist'),
    # path('remove_from_wishlist/<int:wishlist_item_id>/',views.remove_from_wishlist, name='remove_from_wishlist'),
    # path('add_productwishlist/<int:product_id>/', views.add_productwishlist, name='add_productwishlist'),
    # path('remove_all_from_wishlist/', views.remove_all_from_wishlist, name='remove_all_from_wishlist'),


    path('about', views.about, name='about'),
    path('shop', views.shop, name='shop'),
    path('category/vegetables/', views.category_vegetables, name='category_vegetables'),
    path('category/fruits/', views.category_fruits, name='category_fruits'),

    #payment
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('paymentsuccess/', views.paymentsuccess, name='productsuccess'),



    path('live_search/', views.live_search, name='live_search'),
    path('submit_review/', views.submit_review, name='submit_review'),

    # path('add_review/', views.add_review, name='add_review'),

    path('regdelivery', views.regdelivery, name='regdelivery'),
    path('deliveryagent', views.deliveryagent, name='deliveryagent'),
    path('approve_delivery_agent/<int:agent_id>/approve/', views.approve_delivery_agent, name='approve_delivery_agent'),
    path('reject_delivery_agent/<int:agent_id>/reject/', views.reject_delivery_agent, name='reject_delivery_agent'),
    path('deliverylogin', views.deliverylogin, name='deliverylogin'),
    path('deliverydetails', views.deliverydetails, name='deliverydetails'),
    path('delivery_agents/', views.delivery_agents, name='delivery_agents'),




]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)