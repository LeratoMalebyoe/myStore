from django.shortcuts       import render, redirect
from django.contrib import messages
from django.contrib.auth    import authenticate, login, logout
from django.contrib.auth.models import User
from django.http            import HttpResponseRedirect
from django.urls            import reverse
from django.db import IntegrityError

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
            return redirect('personal:home')
        else:
            return render(request, 'user_auth/login.html', {
                'error': 'Invalid username or password'
            })
    return render(request, 'user_auth/login.html')

def authenticate_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST.get('remember')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if not remember:
                request.session.set_expiry(0) #Session expires

            return redirect('store:home') #Auto redirect
        else:
            return render(request, 'user_auth/login.html', {
                'error': 'Invalid username or password'
            })
def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')
        fname = request.POST.get('firstname')
        sname = request.POST.get('surname')

        #Check if username exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'user_auth/signup.html')

        #Check if passwords match
        if pwd1 != pwd2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'user_auth/signup.html')

        #Create user
        user = User.objects.create_user(
            username=uname,
            password=pwd1,
            first_name=fname,
            last_name=sname
        )

        try:
            user = User.objects.create_user(username=uname, password=pwd1, first_name=fname, last_name=sname)
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('store:home')
        except IntegrityError:
            messages.error(request, 'Username is already taken. Please choose another.')
            return render(request, 'user_auth/signup.html')


    return render(request, 'user_auth/signup.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_auth:login'))

def show_user(request):
    return render(request, 'user_auth/user.html', {
        'username': request.user.username,
        'first_name': request.user.first_name
    })
