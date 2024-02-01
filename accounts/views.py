from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group, Permission
from .forms import UserRegistrationForm, StaffUserRegistrationForm
from .models import StaffUser
from django.contrib import messages
from polls.models import Poll 
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next', 'home')
            return redirect(redirect_url)
        else:
            messages.error(request, "Username Or Password is incorrect!",
                           extra_tags='alert alert-warning alert-dismissible fade show')

    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def create_user(request, is_staff):
    is_staff = is_staff.lower()=="true"
    if request.method == 'POST':
        if is_staff:
            form = StaffUserRegistrationForm(request.POST)
        else:
            form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            if is_staff:
                card_number = form.cleaned_data['card_number']
                cardholder_name = form.cleaned_data['cardholder_name']
                expiration_date = form.cleaned_data['expiration_date']
                cvv = form.cleaned_data['cvv']
            if is_staff:
                if StaffUser.objects.filter(user__email=email).exists():
                    messages.error(request, 'Email already registered!', extra_tags='alert alert-warning alert-dismissible fade show')
                    messages.error(request, 'Registration failed!', extra_tags='alert alert-warning alert-dismissible fade show')
                    return redirect('accounts:register')
                else:
                    group, created = Group.objects.get_or_create(name='staff users')
                    content_type = ContentType.objects.get_for_model(Poll)
                    group.permissions.add(
                        Permission.objects.get_or_create(codename="can_view_Poll", name='view poll', content_type=content_type)[0],
                        Permission.objects.get_or_create(codename="can_edit_Poll", name='edit poll', content_type=content_type)[0]
                    )
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password1, email=email)
                    user.is_staff = True
                    user.save()
                    user.groups.add(group)
                    staff_user = StaffUser.objects.create(user=user, card_number=card_number, cardholder_name=cardholder_name, expiration_date=expiration_date, cvv=cvv)
                    staff_user.save()
                    messages.success(request, f'Thanks for registering {user.username}.', extra_tags='alert alert-success alert-dismissible fade show')
                    return redirect('accounts:login')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already registered!', extra_tags='alert alert-warning alert-dismissible fade show')
                    messages.error(request, 'Registration failed!', extra_tags='alert alert-warning alert-dismissible fade show')
                    return redirect('accounts:register')
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password1, email=email)
                    messages.success(request, f'Thanks for registering {user.username}.', extra_tags='alert alert-success alert-dismissible fade show')
                    return redirect('accounts:login')
        else:
            messages.error(request, 'Registration failed!', extra_tags='alert alert-warning alert-dismissible fade show')
    else:
        if is_staff:
            form = StaffUserRegistrationForm(request.POST)
        else:
            form = UserRegistrationForm(request.POST)
    return render(request, 'accounts/register.html', {'form': form})
