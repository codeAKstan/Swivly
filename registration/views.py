from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# Create your views here.

def index(request):
    return render(request,
                  'registration/index.html')

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
    return render(request, 'registration/profile.html',
                  {'section': 'profile'})