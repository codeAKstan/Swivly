from django.shortcuts import render, redirect, get_object_or_404
from .models import House, HouseImage
from .forms import HouseForm, HouseImageForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

# Create your views here.

def accommodation(request):
    return render(request, 'accommodation/accommodation.html')

@login_required
def add_house(request):
    if request.user.profile.role != 'agent':
        messages.error(request, "You are not authorized to add houses. Only agents can perform this action.")
        return redirect('accommodation:accommodation_list')

    if request.method == 'POST':
        house_form = HouseForm(request.POST, request.FILES)
        image_formset = forms.modelformset_factory(HouseImage, form=HouseImageForm, extra=3)
        formset = image_formset(request.POST, request.FILES, queryset=HouseImage.objects.none())

        if house_form.is_valid() and formset.is_valid():
            house = house_form.save(commit=False)
            house.user = request.user
            house.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    HouseImage.objects.create(house=house, image=image)

            messages.success(request, "House added successfully!, awaiting approval")
            return redirect('accommodation:accommodation_list')
    else:
        house_form = HouseForm()
        image_formset = forms.modelformset_factory(HouseImage, form=HouseImageForm, extra=3)
        formset = image_formset(queryset=HouseImage.objects.none())

    return render(request, 'accommodation/add_house.html', {'house_form': house_form, 'formset': formset})


def accommodation_list(request):
    houses = House.objects.filter(is_available=True)  # Only fetch available houses
    return render(request, 'accommodation/accommodation_list.html', {'houses': houses})

def house_detail(request, house_id):
    house = get_object_or_404(House, id=house_id)
    return render(request, 'accommodation/house_detail.html', {'house': house})


@login_required
def listing_summary(request):
    # Ensure only agents can access this page
    if request.user.profile.role != "agent":
        return render(request, 'accommodation/not_authorized.html')

    # Filter houses by the current logged-in agent
    houses = House.objects.filter(user=request.user)

    # Count listings by status
    active_count = houses.filter(is_available=True).count()
    pending_count = houses.filter(is_available=False, created__isnull=False).count()
    rejected_count = houses.filter(is_available=False, created__isnull=True).count()

    context = {
        'houses': houses,
        'active_count': active_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'accommodation/listing_summary.html', context)


@login_required
def edit_listing(request, house_id):
    # Fetch the house for the logged-in agent
    house = get_object_or_404(House, id=house_id, user=request.user)

    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES, instance=house)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing updated successfully!")
            return redirect('accommodation:listing_summary')
    else:
        form = HouseForm(instance=house)

    return render(request, 'accommodation/edit_listing.html', {'form': form, 'house': house})

@login_required
def delete_listing(request, house_id):
    # Fetch the house for the logged-in agent
    house = get_object_or_404(House, id=house_id, user=request.user)

    if request.method == 'POST':
        house.delete()
        messages.success(request, "Listing deleted successfully!")
        return redirect('accommodation:listing_summary')

    return render(request, 'accommodation/confirm_delete.html', {'house': house})