"""eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from mainApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.home),
    path("shop/<str:mc>/<str:sc>/<str:br>/",views.shop),
    path("single-product/<int:id>/",views.singleProduct),
    path("login/",views.loginPage),
    path('logout/',views.logoutPage),
    path("signup/",views.signupPage),
    path('profile/',views.profilePage),
    path('update-profile/',views.updateProfilePage),
    path('add-to-cart/<int:id>/',views.addToCart),
    path('cart-page/',views.cartPage),
    path('delete-cart/<int:id>/',views.deleteCart),
    path('update-cart/<int:id>/<str:action>',views.updateCart),
    path('add-to-wishlist/<int:pid>',views.addToWishlist),
    path('delete-wishlist/<int:id>',views.deleteWishlist),
    path('check-out/',views.checkOut),
    path('order/',views.orderPage),
    path('confirmation/',views.confirmationPage),
    path('contact/',views.contactPage),
    path('search/',views.searchPage),
    path('forget-username/',views.forgetUsername),
    path('enter-otp/',views.enterOtp),
    path('forget-password/',views.forgetPassword),
    path('paymetnSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/',views.paymentSuccess),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
