from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.contrib.auth import login, authenticate, logout
from .models import Cycle, Rental, UserProfile


from .forms import RegisterForm, LoginForm
def home(request):
    return render(request,'landingpg.html')

from .models import UserProfile
from django.contrib.auth import login
from .models import UserProfile

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            is_owner = (user_type == 'owner')
            profile = user.userprofile
            profile.is_owner = is_owner
            profile.save()

            login(request, user)
            return redirect('owner_dashboard' if is_owner else 'user_dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import UserProfile

from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect based on user type
            profile = UserProfile.objects.get(user=user)
            return redirect('owner_dashboard' if profile.is_owner else 'user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def owner_dashboard(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if not profile.is_owner:
        return redirect('user_dashboard')
    
    cycle = Cycle.objects.filter(owner=user).first()
    return render(request, 'owner_dashboard.html', {'cycle': cycle})

def user_dashboard(request):
    return render(request, 'user_dashboard.html')