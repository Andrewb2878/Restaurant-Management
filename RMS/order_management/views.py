from django.shortcuts import render

# Create your views here.
def order_management(request):
    return render(request, 'order_management/order_management.html')