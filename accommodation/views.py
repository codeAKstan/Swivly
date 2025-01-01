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

            messages.success(request, "House added successfully!")
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