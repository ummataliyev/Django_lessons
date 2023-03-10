from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView

from .views import EditUserView
from .views import user_register
from .views import dashboard_view


urlpatterns = [
    # path('login', user_login, name='login')
    # path('signup/', SignUpView.as_view(), name='user_register'),
    # path('profile/edit', edit_user, name='edit_user_information'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'), # noqa
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'), # noqa
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'), # noqa
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'), # noqa
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # noqa
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'), # noqa
    path('profile/', dashboard_view, name='user_profile'),
    path('signup/', user_register, name='user_register'),
    path('profile/edit', EditUserView.as_view(), name='edit_user_information'),
]
