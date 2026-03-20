from django.contrib import admin
from django.urls import path
from users.views import LoginView, SignUpView, UserDetailsView, LogoutView, UserProfileView

"""
URL routing for user-related actions.

Includes paths for authentication (login/logout/signup) and 
profile management (details/profile views).
"""
urlpatterns = [
    #: Login page.
    path('login/', LoginView.as_view(), name='login'),
    #: Registration page.
    path('signup/', SignUpView.as_view(), name='signup'),
    #: Public or personal profile view.
    path('profile/', UserProfileView.as_view(), name='profile'),
    #: Settings page for updating account details.
    path('details/', UserDetailsView.as_view(), name='details'),
    #: Logout action.
    path('logout/', LogoutView.as_view(), name='logout'),
]