from django.urls import path

from .views import Signup, Login, Logout, upgrade_me

app_name = 'account'

urlpatterns = [
    path("signup/", Signup.as_view(), name="accounts_signup"),
    path("login/", Login.as_view(), name="accounts_login"),
    path("logout/", Logout.as_view(), name="account_logout"),
    path("upgrade/", upgrade_me, name='upgrade'),
]