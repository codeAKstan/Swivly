from django.shortcuts import render, redirect
from .models import House, HouseImage
from .forms import HouseForm, HouseImageForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def accommodation(request):
    return render(request, 'registration/accommodation.html')

@login_required
def add_house(request):
    if not request.user.profile.role in ['agent']:
        messages.success(request, "you are not an agent")
    if request.method == 'POST':
        house_form = HouseForm(request.POST, request.FILES)
        image_formset = forms.modelformset_factory(HouseImage, form=HouseImageForm, extra=3)
        formset = image_formset(request.POST, request.FILES, queryset=HouseImage.objects.none())

        if house_form.is_valid() and formset.is_valid():
            house = house_form.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    HouseImage.objects.create(house=house, image=image)

            return redirect('accommodation_list')  # Redirect to accommodation list
    else:
        house_form = HouseForm()
        image_formset = forms.modelformset_factory(HouseImage, form=HouseImageForm, extra=3)
        formset = image_formset(queryset=HouseImage.objects.none())

    return render(request, 'registration/add_house.html', {'house_form': house_form, 'formset': formset})


def accommodation_list(request):
    houses = House.objects.filter(is_available=True)
    return render(request, 'registration/accommodation_list.html', {'houses': houses})
