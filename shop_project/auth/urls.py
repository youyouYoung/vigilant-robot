from django.urls import include, path, re_path
from .views import GoogleLogin, GoogleLoginCallback, LoginPage
from allauth.account.views import ConfirmEmailView

urlpatterns = [
    path("login/", LoginPage.as_view(), name="login"),
    re_path(r"^accounts/", include("allauth.urls")),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path(
        "google/callback/",
        GoogleLoginCallback.as_view(),
        name="google_login_callback",
    ),
    path("registration/", include("dj_rest_auth.registration.urls")),
    re_path(
        "^registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("", include("dj_rest_auth.urls")),
]