from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("join/", views.JoinView.as_view(), name="register"),
    path("join/pending/", views.JoinPendingView.as_view(), name="join_pending"),
    path("join/invite/<uuid:token>/", views.InvitationAcceptView.as_view(), name="invitation_accept"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    path("profile/<str:username>/", views.ProfileView.as_view(), name="profile"),
]
