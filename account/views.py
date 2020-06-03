from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
###########################################login/register#################################################

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user  = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account Created Successfully for '+ username)
            return redirect('login')

    context = {'form':form}
    return render (request, 'account/register.htm', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'username or password is incorrect')

    context = {}
    return render (request, 'account/login.htm', context)



def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    
    total_orders = orders.count()
    pending = orders.filter(status="Pending").count()   
    delivered = orders.filter(status="Delivered").count()

    print("Orders: ", orders)
    context = {
        'orders': orders,       
        'total_orders':total_orders,
        'pending':pending,
        'delivered':delivered,
        }
    return render(request, 'account/user.htm', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid:
            form.save()

    context = {'form':form}
    return render(request, 'account/account_settings.htm', context)


##########################################################################################################

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    pending = orders.filter(status="Pending").count()
    delivered = orders.filter(status="Delivered").count()

    context = {
        'orders': orders,
        'customers':customers,
        'total_orders':total_orders,
        'pending':pending,
        'delivered':delivered,
        }
    return render(request, 'account/dashboard.htm', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'account/products.htm', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter,
    }
    return render(request, 'account/customer.htm', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset= Order.objects.none(), instance = customer)
    # form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        # print('Printing Post: ', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    
    context = {
        'customer':customer,
        'formset': formset,
    }
    return render (request, 'account/order_form.htm', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
    }
    return render (request, 'account/order_form.htm', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {
        'item': order,
    }
    return render(request, 'account/delete.htm', context)