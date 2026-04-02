"""
URL routing for user-related actions.

Includes paths for authentication (login/logout/signup) and
profile management (details/profile views).
"""
from django.urls import path
from users.views import LoginView, SignUpView, LogoutView, UserProfileView, UserProfileEditView


urlpatterns = [
    #: Login page.
    path('login/', LoginView.as_view(), name='login'),
    #: Registration page.
    path('signup/', SignUpView.as_view(), name='signup'),
    #: Public or personal profile view.
    path('profile/', UserProfileView.as_view(), name='profile'),
    #: Settings page for updating account details.
    path('edit/', UserProfileEditView.as_view(), name='edit_profile'),
    #: Logout action.
    path('logout/', LogoutView.as_view(), name='logout'),
]
