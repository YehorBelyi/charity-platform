from django.contrib import admin
from django.urls import path
from users.views import LoginView, SignUpView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
]