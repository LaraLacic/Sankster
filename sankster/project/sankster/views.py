from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from .models import MenuItem, Order, OrderItem, CustomUser
from .forms import MenuItemForm, OrderItemForm, EditStaffForm, CreateStaffForm

User = get_user_model()

def is_admin(user):
    return user.is_superuser

def home(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'home.html', {'menu_items' : menu_items})

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'barista':
        return redirect('barista_dashboard')
    elif user.role == 'server':
        return redirect('server_dashboard')
    else:
        return redirect('home')


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('dashboard') 
    return render(request, 'admin_dashboard.html')

@login_required
def barista_dashboard(request):
    if request.user.role != 'barista':
        return redirect('dashboard')

    active_orders = Order.objects.filter(is_active=True, status='received').order_by('-id')
    return render(request, 'barista_dashboard.html', {'active_orders' : active_orders})

@login_required
def server_dashboard(request):
    if request.user.role != 'server':
        return redirect('dashboard')
    active_orders = Order.objects.filter(is_active = True).order_by('-id')
    return render(request, 'server_dashboard.html', {'active_orders': active_orders})    


@login_required
@user_passes_test(is_admin)
def manage_menu(request):
    menu_items = MenuItem.objects.all()
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_menu')
    else:
        form = MenuItemForm()

    return render(request, 'manage_menu.html', {'menu_items': menu_items, 'form': form})

@login_required
@user_passes_test(is_admin)
def delete_menu_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(MenuItem, id=item_id)
        item.delete()
    return redirect('manage_menu')

@login_required
@user_passes_test(is_admin)
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('manage_menu')
    else:
        form = MenuItemForm(instance=item)
    
    return render(request, 'edit_menu_item.html', {'form': form, 'item': item})

@login_required
@user_passes_test(is_admin)
def create_worker(request):
    if request.method == 'POST':
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_staff')
    else:
        form = CreateStaffForm()
    return render(request, 'create_worker.html', {'form': form})

def edit_worker(request, worker_id):
    worker = get_object_or_404(CustomUser, id=worker_id)
    if request.method == 'POST':
        form = EditStaffForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            return redirect('manage_staff')
    else:
        form = EditStaffForm(instance=worker)

    return render(request, 'edit_worker.html',{'form':form, 'worker':worker})

  
def manage_staff(request):
    employees = CustomUser.objects.all() 
    return render(request, 'manage_staff.html', {'employees': employees})


def create_order(request):
    if request.user.role != 'server':
        return redirect('dashboard')
    
    order = Order.objects.create(
        server = request.user,
        status = 'received',
        is_active=True
    )
    return redirect('order_detail', order_id=order.id)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.server.username == 'guest_server' and request.user.role == 'server':
        order.server = request.user
        order.save()

    if order.server != request.user:
        return redirect('dashboard')

    if request.method == 'POST':

        table_number = request.POST.get("table_number")
        if table_number:
            order.table_number = table_number
            order.save()

        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            return redirect('order_detail', order_id = order.id)
    else:
        form = OrderItemForm()
    
    return render(request, 'order_detail.html', {'form': form, 'order': order})


@login_required
def update_order_status(request, order_id):
    if request.user.role != 'barista':
        return redirect('dashboard')

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
    
    return redirect('barista_dashboard')


def get_order_status(request):
    if request.user.is_authenticated and request.user.role == 'server':
        orders = Order.objects.filter(server=request.user)
        data = [{"id": order.id, "status": order.status} for order in orders]
        return JsonResponse({"orders": data})
    return JsonResponse({"error": "Unauthorized"}, status=403)


@login_required
def mark_order_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.user.role != 'server':
        return redirect('dashboard')

    if request.method == 'POST':
        order.is_active = False
        order.status = 'ready'
        order.save()
        order.delete()
        return redirect('server_dashboard')


def call_server(request):
    if request.method == "POST":
        table_number = request.POST.get("table_number")
        if not table_number or not table_number.isdigit() or int(table_number) <= 0:
            messages.error(request, "Molimo unesite ispravan broj stola (pozitivan cijeli broj).")
            return redirect('home')

        guest_user = User.objects.get(username='guest_server')
        Order.objects.create(server=guest_user, status="pending", table_number=table_number)  
    return redirect('home')
    

@login_required
def mark_order_received(request, order_id):
    if request.user.role != 'server':
        return redirect('dashboard')

    order = get_object_or_404(Order, id=order_id)
    if order.status != 'received': 
        order.status = 'received' 
        order.save()
    
    return redirect('server_dashboard')
