from django.shortcuts import render
from django.views import View
from users.forms import UserSignupForm, TemplateForm


# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

class SignUpView(View):
    template_name = 'users/signup.html'

    def get(self, request):

        context = {
            "form" : UserSignupForm,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = UserSignupForm(request.POST)

        if form.is_valid():
            form.save()

        return render(request, self.template_name)

    # template_name = 'authentication/login.html'
    # form_class = forms.LoginForm
    #
    # def get(self, request):
    #     form = self.form_class()
    #     message = ''
    #     return render(request, self.template_name, context={'form': form, 'message': message})
    #
    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         user = authenticate(
    #             username=form.cleaned_data['username'],
    #             password=form.cleaned_data['password'],
    #         )
    #         if user is not None:
    #             login(request, user)
    #             return redirect('home')
    #     message = 'Login failed!'
    #     return render(request, self.template_name, context={'form': form, 'message': message})