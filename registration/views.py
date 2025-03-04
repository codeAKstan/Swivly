from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserEditForm, ProfileEditForm, ProductForm, ProductImageForm, ServiceForm
from .models import Listing, Transaction, Profile, Category, Product, ProductImage, Service, ServiceCategory
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from orders.models import Order, OrderItem
from django.forms import modelformset_factory
from django import forms
from django.db import IntegrityError
import requests
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.

# def index(request):
#     return render(request,
#                   'registration/index.html')

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

            # Ensure the profile does not already exist
            try:
                Profile.objects.create(user=new_user, role=form.cleaned_data['role'])
            except IntegrityError:
                messages.success(request, "profile created login.")
                return render(request, 'registration/login.html', {'form': login_form})

            return render(request, 'registration/login.html', {'new_user': new_user, 'form': login_form})
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    

@login_required
def profile(request):
    role = request.user.profile.role


    if role == "buyer":
        transactions = Order.objects.filter(user=request.user).order_by('-created')
    else:
        transactions = []

    return render(request, 'registration/profile.html', {
        'transactions': transactions,
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


def product_list_or_index(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get('search', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        

    template = 'registration/shop.html' if 'shop' in request.path else 'registration/index.html'

    return render(request, template, {
        'category': category,
        'categories': categories,
        'products': products,
        'page_obj': page_obj,
        'query': query,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    images = product.images.all()
    return render(request,
                  'registration/detail.html',
                  {'product': product,
                   'images':images})

def market_place(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    query = request.GET.get('search', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        

    return render(request, 'registration/shop.html', {
        'categories': categories,
        'products': products,
        'page_obj': page_obj,
        'query': query, 
    })



@login_required
def add_product(request):
    if not request.user.profile.role in ['seller', 'agent']:
        return redirect('registration:login')

    ProductImageFormSet = modelformset_factory(ProductImage, fields=('image',), extra=5)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())

        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    ProductImage.objects.create(product=product, image=image)

            messages.success(request, "Product added successfully!")
            return redirect('registration:listing_summary')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm()
        formset = ProductImageFormSet(queryset=ProductImage.objects.none())

    return render(request, 'registration/product_upload.html', {
        'form': form,
        'formset': formset,
    })



def listing_summary(request):
    if not request.user.is_authenticated:
        return redirect('registration:login')

    # Ensure the user is a seller or agent
    if request.user.profile.role not in ['seller', 'agent']:
        return redirect('registration:dashboard')

    products = Product.objects.filter(user=request.user)
    active_count = products.filter(available=True).count()
    pending_count = products.filter(status='pending').count()
    rejected_count = products.filter(status='rejected').count()

    context = {
        'active_count': active_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'products': products,
    }
    return render(request, 'registration/listing_summary.html', context)


def services(request):
    services = Service.objects.all()
    categories = ServiceCategory.objects.all()

    search_term = request.GET.get('search')
    category_id = request.GET.get('category')

    if search_term:
        services = services.filter(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
        )
    if category_id:
        services = services.filter(category_id=category_id)
    return render(request, 'registration/services.html',
                  {'services': services,
                   'categories': categories})
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    return render(request, 'registration/service_detail.html',
                  {'service': service})

@login_required
def add_service(request):
    if not request.session.get('has_paid', False):
        return HttpResponseRedirect('/pay/')
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_by = request.user
            service.save()
            # Reset the payment session after successfully adding a service
            request.session['has_paid'] = False
            return redirect('registration:services')
    else:
        form = ServiceForm()
    return render(request, 'registration/add_service.html', {'form': form})



@login_required
def payment_page(request):
    paystack_url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": request.user.email,
        "amount": 50000,
        "callback_url": "http://127.0.0.1:8000/payment/callback/",
    }

    response = requests.post(paystack_url, headers=headers, json=data)
    result = response.json()

    if result.get("status") == True:
        # Redirect to the Paystack payment page
        payment_url = result["data"]["authorization_url"]
        return HttpResponseRedirect(payment_url)
    else:
        return JsonResponse({"error": "Payment initialization failed"}, status=400)


@login_required
def payment_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        return JsonResponse({"error": "Transaction reference is missing"}, status=400)

    # Verify the payment with Paystack
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    response = requests.get(url, headers=headers)
    result = response.json()

    if result.get("status") == True and result["data"]["status"] == "success":
        # Payment is successful
        # Set the session to indicate the user has paid
        request.session['has_paid'] = True
        # Redirect to the add service page
        return HttpResponseRedirect('/add/')
    else:
        # Payment failed
        return JsonResponse({"error": "Payment verification failed"}, status=400)
