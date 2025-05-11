from django.shortcuts import render, redirect
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm  
from core.models import MenuItem, UserProfile  
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from decimal import Decimal
from django.contrib import messages  
from django.contrib.auth.models import User  

# Check if the user is a waiter
def is_waiter(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == "Waiter"


@login_required
@user_passes_test(is_waiter)  # Restrict access to waiters
def order_management(request):
    orders = Order.objects.all()
    menu_items = MenuItem.objects.all()

    order_form = OrderForm(initial={'table_number': request.session.get("table_number", "")})  # Retain table number
    order_item_form = OrderItemForm()
    total_price = float(request.session.get("total_price", 0))
    order_items = request.session.get("order_items", [])

    if request.method == "POST":
        if "add_item" in request.POST:
            try:
                menu_item_id = request.POST.get("menu_item")
                quantity = int(request.POST.get("quantity", 1))

                if menu_item_id:
                    menu_item = MenuItem.objects.get(id=menu_item_id)

                    request.session["table_number"] = request.POST.get("table_number", request.session.get("table_number", ""))

                    order_items.append({
                        "menu_item_id": menu_item.id,
                        "menu_item": menu_item.name,
                        "price": float(menu_item.price),
                        "quantity": quantity,
                    })

                    request.session["order_items"] = order_items
                    request.session["total_price"] = sum(item["price"] * item["quantity"] for item in order_items)
                    messages.success(request, f"{quantity} x {menu_item.name} added!")
                else:
                    messages.error(request, "Please select a menu item.")
            except MenuItem.DoesNotExist:
                messages.error(request, "The selected menu item does not exist.")
                return redirect("order_management")

        elif "clear_items" in request.POST:
            request.session.pop("order_items", None)  # Remove saved items
            request.session.pop("total_price", None)  # Reset total price
            messages.success(request, "Current items have been cleared!")
            return redirect("order_management")

        elif "create_order" in request.POST:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.waiter = request.user  
                order.payment_status = "unpaid"
                order.table_number = request.session.get("table_number")
                order.save()

                # Save stored items in order
                for item in request.session.get("order_items", []):
                    OrderItem.objects.create(
                        order=order,
                        menu_item=MenuItem.objects.get(id=item["menu_item_id"]),
                        quantity=item["quantity"]
                    )

                # Clear session data after successful order creation
                request.session.pop("order_items", None)
                request.session.pop("total_price", None)
                request.session.pop("table_number", None)
                
                messages.success(request, f"Order #{order.id} created!")
                return redirect("order_management")
            else:
                messages.error(request, "Error creating order. Please check the form.")

    return render(request, "order_management/order_management.html", {
        "orders": orders,
        "menu_items": menu_items,
        "order_form": order_form,
        "order_item_form": order_item_form,
        "order_items": order_items,
        "total_price": total_price,
        "order_status_choices": Order.STATUS_CHOICES,
    })
