from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserEditForm, ProfileEditForm
from .models import Listing, Transaction, Profile
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request,
                  'registration/index.html')

def about_us(request):
    return render(request,
                  'registration/about.html')

# register view
def register(request):
    role = request.GET.get('role')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login_form = AuthenticationForm()
            Profile.objects.create(user=new_user)
            return render(request, 'registration/login.html', {'new_user': new_user, 'form': login_form})
        else:
            return render(request, 'registration/register.html',
                      {'form':form})
    else:
        form = UserRegisterForm()
        return render(request, 'registration/register.html',
                      {'form':form})
    


@login_required
def profile(request):
    role = request.user.profile.role

    # Data for sellers/agents
    if role in ["agent", "seller"]:
        active_listings_count = Listing.objects.filter(user=request.user, status="active").count()
        pending_listings_count = Listing.objects.filter(user=request.user, status="pending").count()
        expired_listings_count = Listing.objects.filter(user=request.user, status="expired").count()
    else:
        active_listings_count = pending_listings_count = expired_listings_count = 0

    # Data for buyers
    if role == "buyer":
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    else:
        transactions = []

    return render(request, 'registration/profile.html', {
        'active_listings_count': active_listings_count,
        'pending_listings_count': pending_listings_count,
        'expired_listings_count': expired_listings_count,
        'transactions': transactions
    })


def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('registration:profile')
        else:
            messages.error(request, 'Error Updating Profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 
                  'registration/edit.html',
                {'user_form': user_form,
                'profile_form': profile_form})
