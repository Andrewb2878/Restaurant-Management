from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import MenuItem  # Import your model

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def menu(request):
    # Fetch available menu items from the database
    menu_items = MenuItem.objects.filter(available=True)  
    # Pass the data to the template
    return render(request, 'core/menu.html', {'menu_items': menu_items})

def portal(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return redirect("posts:list")
    else:
        form = AuthenticationForm()
    return render(request, 'core/portal.html', {"form": form})