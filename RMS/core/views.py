from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
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

def portal_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/portal.html')