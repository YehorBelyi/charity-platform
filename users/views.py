from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from donations.models import Payment
from users.forms import UserLoginForm, UserSignUpForm, UserUpdateForm


# Create your views here.
class LoginView(View):
    """Handles user authentication and session creation."""
    template_name = 'users/login.html'

    def get(self, request):
        """Display the login form."""
        form = UserLoginForm(request.GET or None)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Validate credentials and log the user in."""
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Wrong username or password!')

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class SignUpView(View):
    """Handles new user registration."""
    template_name = 'users/signup.html'

    def get(self, request):
        form = UserSignUpForm(request.GET or None)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Create a new user instance and log them in upon success."""
        form = UserSignUpForm(request.POST, request.FILES)

        context = {
            'form': form,
        }

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            login(request, user)
            return redirect('home')

        return render(request, self.template_name, context)


class LogoutView(View):
    template_name = 'pages/index.html'

    def post(self, request):
        logout(request)
        return render(request, self.template_name)


class UserProfileView(LoginRequiredMixin, View):
    """Displays the user's public profile and donation history."""
    template_name = 'users/profile.html'
    login_url = 'login'

    def get(self, request):
        """
        Fetch user details and finished payment history.

        Context Includes:
            history: Prefetched list of successful payments.
        """
        current_user = request.user

        context = {
            'username': current_user.username,
            'full_name': f"{current_user.first_name} {current_user.last_name}",
            'status': current_user.get_status_display(),
            'rank': current_user.get_rank_display(),
            'phone_number': current_user.phone_number,
            'avatar': current_user.avatar.url if current_user.avatar else None,
            'short_bio': current_user.short_bio,
        }
        return render(request, self.template_name, context)


class UserProfileEditView(LoginRequiredMixin, View):
    """Displays the user's profile full details."""
    template_name = 'components/profile_edit_form.html'

    def get(self, request):
        """Get user profile details."""
        form = UserUpdateForm(instance=request.user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        """Update user profile details."""

        def post(self, request):
            form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

            if form.is_valid():
                form.save()

                request.user.refresh_from_db()

                context = {
                    'username': request.user.username,
                    'full_name': f"{request.user.first_name or ''} {request.user.last_name or ''}".strip(),
                    'status': request.user.get_status_display(),
                    'rank': request.user.get_rank_display(),
                    'phone_number': request.user.phone_number,
                    'avatar': request.user.avatar.url if request.user.avatar else None,
                    'short_bio': request.user.short_bio,
                }

                response = HttpResponse(request, 'components/user_profile.html', context)
                response['HX-Trigger'] = 'profileUpdated'
                return response

            print(form.errors)
            return render(request, self.template_name, {'form': form})
