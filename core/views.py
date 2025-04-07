from decimal import Decimal
from django.shortcuts import redirect,render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .models import Cycle, Rental, UserProfile, CycleReview
from django.db.models import Avg
from .forms import RegisterForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def home(request):
    return render(request,'landingpg.html')

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
            return redirect('account_setup')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            profile = UserProfile.objects.get(user=user)
            if not profile.details_completed:
                return redirect('account_setup')
            return redirect('owner_dashboard' if profile.is_owner else 'user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
@csrf_exempt
def account_setup(request):
    profile = UserProfile.objects.get(user=request.user)
    user = request.user

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        phone = request.POST.get('phone_number')
        profile.phone_number = phone
        profile.details_completed = True
        profile.save()

        if profile.is_owner:
            name = request.POST.get('name')
            rate =request.POST.get('rate')
            lat = request.POST.get('lat')
            lng = request.POST.get('lng')
            description = request.POST.get('description')

            Cycle.objects.create(
                owner=user,
                name=name,
                rate_per_hour=rate,
                location_lat=lat,
                location_lng=lng,
                description=description,
                is_available=True 
            )

        return redirect('owner_dashboard' if profile.is_owner else 'user_dashboard')

    return render(request, 'account_setup.html', {'profile': profile})

@csrf_exempt
@login_required
def edit_cycle(request, cycle_id):
    if request.method == 'POST':
        try:
            cycle = Cycle.objects.get(id=cycle_id, owner=request.user)
            data = json.loads(request.body)

            cycle.description = data.get('description', cycle.description)
            cycle.is_available = data.get('is_available', cycle.is_available)

            if 'latitude' in data and 'longitude' in data:
                cycle.latitude = data['latitude']
                cycle.longitude = data['longitude']

            cycle.save()

            return JsonResponse({'status': 'success'})
        except Cycle.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cycle not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)


@csrf_exempt
@login_required
def remove_listing(request, cycle_id):
    if request.method == 'POST':
        try:
            cycle = Cycle.objects.get(id=cycle_id, owner=request.user)
            cycle.is_available = False
            cycle.save()
            return JsonResponse({'success': True})
        except Cycle.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cycle not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)

@csrf_exempt
@login_required
def relist_cycle(request, cycle_id):
    if request.method == 'POST':
        try:
            cycle = Cycle.objects.get(id=cycle_id, owner=request.user)
            cycle.is_available = True
            cycle.save()
            return JsonResponse({'success': True})
        except Cycle.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cycle not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)

def owner_dashboard(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if not profile.is_owner:
        return redirect('user_dashboard')
    
    cycle = Cycle.objects.filter(owner=user).first()

    reviews = []
    avg_rating = 0
    latest_reviews = []

    if cycle:
        reviews = cycle.reviews.all().order_by('-timestamp')
        avg_rating = reviews.aggregate(avg=Avg('stars'))['avg'] or 0
        avg_rating = round(avg_rating, 1)
        latest_reviews = reviews[:3]

    context = {
        'cycle': cycle,
        'avg_rating': avg_rating,
        'latest_reviews': latest_reviews,
    }

    return render(request, 'owner_dashboard.html', context)


def user_dashboard(request):
    return render(request, 'user_dashboard.html')

def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')

def logout_view(request):
    logout(request)
    return redirect('home')
