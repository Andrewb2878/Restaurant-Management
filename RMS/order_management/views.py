from django.shortcuts import render, redirect
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm  
from core.models import MenuItem, UserProfile  
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from decimal import Decimal
from django.contrib import messages  
from django.contrib.auth.models import User 
from django.shortcuts import get_object_or_404

# Check if the user is a waiter
def is_waiter(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == "Waiter"

def is_chef_or_waiter(user):
    return user.is_authenticated and (
        hasattr(user, 'userprofile') and user.userprofile.role in ["Chef", "Waiter"]
    )

@login_required
@user_passes_test(is_chef_or_waiter)
def view_order_items(request, order_id):
    """Fetch order items dynamically."""
    order = get_object_or_404(Order, id=order_id)  # Ensures order exists
    items = order.items.all()  # Fetch related order items using 'items' related_name

    items_data = [
        {"menu_item": item.menu_item.name, "quantity": item.quantity, "price": item.menu_item.price}
        for item in items
    ]

    return JsonResponse({"order_id": order.id, "items": items_data})


@login_required
def update_order_status(request, order_id):
    if request.method == "POST":
        try:
            import json
            body = json.loads(request.body)
            new_status = body.get("status")

            # Validate the new status
            if new_status not in ["pending", "preparing", "ready", "served", "payment"]:
                return JsonResponse({"success": False, "error": "Invalid status"}, status=400)

            # Update the order status
            order = get_object_or_404(Order, id=order_id)
            order.status = new_status
            order.save()

            return JsonResponse({"success": True, "new_status": new_status})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON body"}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)
@login_required
@user_passes_test(is_waiter)  # Restrict access to waiters
def order_management(request):
    # Get the status filter from the query parameters
    status_filter = request.GET.get("status", "all")
    orders = Order.objects.all()

    # Filter orders based on the selected status
    if status_filter == "pending":
        orders = orders.filter(status="pending")
    elif status_filter == "preparing":
        orders = orders.filter(status="preparing")
    elif status_filter == "ready":
        orders = orders.filter(status="ready")
    elif status_filter == "served":
        orders = orders.filter(status="served")

    # Get counts for each status
    pending_orders = Order.objects.filter(status="pending")
    preparing_orders = Order.objects.filter(status="preparing")
    ready_orders = Order.objects.filter(status="ready")
    served_orders = Order.objects.filter(status="served")

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
        "pending_orders": pending_orders,
        "preparing_orders": preparing_orders,
        "ready_orders": ready_orders,
        "served_orders": served_orders,
        "order_status_choices": Order.STATUS_CHOICES,
    })