from django.shortcuts import render
from .models import MenuItem  # Import your model

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def menu(request):
    # Fetch available menu items from the database
    menu_items = MenuItem.objects.filter(available=True)  
    # Pass the data to the template
    return render(request, 'core/menu.html', {'menu_items': menu_items})