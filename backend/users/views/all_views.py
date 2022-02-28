from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from ..forms.login_forms import CreateUserForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from ..models import CustomUser

# 1 x temp 'landing view'
# 3 x register views: register, register done,
# 4 x basic views: login, logout, change password, change password done,
# 4 x password reset views


##replace with real collectr_app landing page.
def landing(request):
    return HttpResponse("Users app dummy landing page")

# login uses uncustomised default view, see urls.py.

# logout uses uncustomised default view, see urls.py.


def register(request):

    if request.user.is_authenticated:
        return redirect('fake_landing')

    if request.method == 'POST':
        f = CreateUserForm(request.POST)
        if f.is_valid():
            f.save(request)
            messages.success(request, 'Account created, check email for activation link.')
            return redirect('login')

    else:
        f = CreateUserForm()

    # return render(request, 'register.html', {'form': f})
    return JsonResponse()


def register_complete(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if (user is not None and default_token_generator.check_token(user, token)):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.INFO, 'Account activated. Please login')
    else:
        messages.add_message(request, messages.INFO, 'Link expired, try again.')

    return redirect('login')
