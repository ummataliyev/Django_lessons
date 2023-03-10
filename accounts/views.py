from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic import CreateView
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile
from .forms import LoginForm
from .forms import UserEditForm
from .forms import ProfileEditForm
from .forms import UserRegistrationForm


# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Login successfully !')

                else:
                    return HttpResponse('Your profile is not active !')

            else:
                return HttpResponse('Login or password is incorrect !')

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {"form": form})


@login_required
def dashboard_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    print(profile)
    context = {
        'user': user,
        'profile': profile
    }

    return render(request, 'pages/user_profile.html', context)


@login_required
def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                "new_user": new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()
        context = {
            "user_form": user_form
        }
        return render(request, 'account/register.html', context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'


# class SignUpView(View):

#     def get(self, request):
#         user_form = UserRegistrationForm()
#         context = {
#             "user_form": user_form
#         }
#         return render(request, 'account/register.html', context)

#     def post(self, request):
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(
#                 user_form.cleaned_data["password"]
#             )
#             new_user.save()
#             context = {
#                 "new_user": new_user
#             }
#             return render(request, 'account/register_done.html', context)


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST) # noqa
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES) # noqa
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/profile_edit.html', {"user_form": user_form, 'profile_form': profile_form}) # noqa


class EditUserView(LoginRequiredMixin, View):

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/profile_edit.html', {"user_form": user_form, 'profile_form': profile_form}) # noqa

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES) # noqa
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
