from django.contrib.auth import authenticate, login, logout
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
        form = UserSignUpForm(request.POST)

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
        history = Payment.objects.prefetch_related("user").filter(user=current_user).filter(is_finished=True)

        context = {
            'username': current_user.username,
            'full_name': f"{current_user.first_name} {current_user.last_name}",
            'status': current_user.get_status_display(),
            'rank': current_user.get_rank_display(),
            'phone_number': current_user.phone_number,
            'avatar' : current_user.avatar.url,
            'history': history,
        }
        return render(request, self.template_name, context)


class UserDetailsView(LoginRequiredMixin, View):
    template_name = 'users/details.html'
    login_url = 'login'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('details')

        context = {'form': form}
        return render(request, self.template_name, context)



