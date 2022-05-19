from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import UserRegisterForm
from django.contrib.auth import logout

# Create your views here.
def login_site(request,*args,**kwargs):
    return render(request, "index.html")

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
    messages.info(request, f'Logged out successfully!')
    return redirect('login')