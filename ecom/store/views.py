from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django import forms
from django.views.generic import DetailView


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have been Logged In')
            return redirect('home')
        else:
            messages.success(request, 'There was an error, retry')
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, ' User Has Updated')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})

    else:
        messages.success(request, 'You Must Be Logged In to Access that page')
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        # Check If They Filled Form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is valid
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Password Has Updated')
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged To Account")
        return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered"))
            return redirect('home')
        else:
            messages.success(request, 'Error, try again')
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})


def category(request, foo):
    foo = foo.replace('-', ' ')
    # Grab Category from URL
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, 'That category does not exist')
        return redirect('home')
