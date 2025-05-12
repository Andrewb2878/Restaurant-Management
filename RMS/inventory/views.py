from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from .models import InventoryItem  
from .forms import QuickOrderForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now

def is_manager(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == "Manager"

@login_required
@user_passes_test(is_manager)  # Restrict access to managers
def inventory(request):
    # Query all inventory items
    inventory_items = InventoryItem.objects.all()

    # Instantiate the Quick Order form
    quick_order_form = QuickOrderForm()

    # Pass the inventory items and form to the template
    return render(request, 'inventory/inventory.html', {
        'inventory_items': inventory_items,
        'quick_order_form': quick_order_form,
    })



@login_required
@user_passes_test(is_manager)
def add_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        unit = request.POST.get("unit")
        min_level = request.POST.get("min_level")
        supplier = request.POST.get("supplier")

        InventoryItem.objects.create(
            name=name,
            quantity=quantity,
            unit=unit,
            min_level=min_level,
            supplier=supplier,
            last_ordered=now() # Set the last ordered date to now
        )
        messages.success(request, f"Item '{name}' added successfully.")
    return redirect("inventory")

@login_required
@user_passes_test(is_manager)
def update_inventory(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        quantity = request.POST.get("quantity")
        min_level = request.POST.get("min_level")
        supplier = request.POST.get("supplier")

        try:
            item = InventoryItem.objects.get(id=item_id)
            item.quantity = quantity
            item.min_level = min_level
            item.supplier = supplier
            item.save()
            messages.success(request, f"{item.name} updated successfully.")
        except InventoryItem.DoesNotExist:
            messages.error(request, "Item not found.")

    return redirect("inventory")

@login_required
@user_passes_test(is_manager)  # Restrict access to managers
def place_order(request):
    if request.method == "POST":
        form = QuickOrderForm(request.POST)
        if form.is_valid():
            # Process the form data
            item = form.cleaned_data['item']
            quantity = form.cleaned_data['quantity']
            supplier = form.cleaned_data['supplier']

            # Update the inventory or perform other actions
            item.quantity += quantity  #  Add the ordered quantity to the inventory
            item.last_ordered = now() # Update the last ordered date
            item.save()
           
               
            messages.success(request, f"Order placed successfully for {quantity} {item.unit} of {item.name}.")
            return redirect('inventory')  # Redirect to the inventory page
        else:
            messages.error(request, "There was an error with your order. Please try again.")
    else:
        form = QuickOrderForm()

    return render(request, 'inventory/inventory.html', {'quick_order_form': form})