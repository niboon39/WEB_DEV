from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {'form': form})

def logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required
def home_site(request,*args,**kwargs):
    #print(request.user.email)
    name = request.user.username

    return render(request, "home_site.html")
