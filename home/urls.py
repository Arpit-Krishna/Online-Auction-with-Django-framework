from django.contrib import admin
from django.urls import path
from home import views
from .views import RegisterView
from django.contrib.auth import views as auth_views
from home.views import CustomLoginView ,ResetPasswordView,user_profile
from home.forms import LoginForm
from home.views import ChangePasswordView

urlpatterns = [
    path("", views.index,name='home'),
    path("about/", views.about,name='about'),
    path("services/", views.services,name='services'),
    path("contact/", views.contact,name='contact'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('bidders-login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='Bidderlogin.html',authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path("Your_orders/",views.logout,name='log_out'),
    path("user_auctions/",views.auction,name='auction'),
    path('add_Item/', views.add_product, name='add_product'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', user_profile, name='users-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]




#path("bidders-login/",views.b_login,name='b_login'),