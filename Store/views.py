from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from . models import Cart,Product,Customer,Payment,OrderPlaced,Wishlist
from django.db.models import Count
from .forms import CustomerRegistrationForm,CustomerProfileForm,ContactForm
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET
from django.conf import settings
import razorpay
from razorpay import Client
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

def index(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))   
    return render(request,"index.html",locals())

@login_required
def about(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))   
        return render(request,"about.html",locals())

@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))   
    return render(request,"contact.html",locals())

def contact_success_view(request):
    return render(request, 'contact_success.html')


@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))   
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,"category.html",locals())


@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))   
        return render(request,"category.html",locals())



@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        wishlist=Wishlist.objects.filter(Q(product=product)&Q(user=request.user))
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))   
        return render(request,"productdetail.html",locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm() 
        return render(request, "customer_register.html", {'form': form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully")
        else:
            messages.warning(request, "Invalid input data")
        return render(request, "customer_register.html", {'form': form})


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))   
        return render(request, 'profile.html',locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Saved Successfully")
            return redirect('profile')  
        else:
            messages.warning(request, "Invalid Input Data!")
        
        return render(request, 'profile.html', {'form': form},locals())

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))   
    return render(request,'address.html',locals())


@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))   
        return render(request,'updateAddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            return redirect('/address')
            messages.success(request,"Congratulations!Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'updateAddress.html',locals())


@login_required
def add_to_cart(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))   
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    
    totalamount = amount + 40
    total_quantity = sum(item.quantity for item in cart)
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))   
    return render(request, 'addtocart.html', locals())


def plus_cart(request):
    prod_id = request.GET.get('prod_id')  
    carts = Cart.objects.filter(product_id=prod_id, user=request.user)
    
    for cart in carts:
        cart.quantity += 1
        cart.save()
    
    total_quantity = sum(cart.quantity for cart in carts)
    total_amount = sum(cart.quantity * cart.product.discounted_price for cart in carts)
    total_amount = calculate_total_amount(request.user)  
    
    data = {
        'quantity': total_quantity,
        'amount': total_amount,
        'totalamount': total_amount,
    }
    
    return redirect("/cart")


def calculate_total_amount(user):
    cart_items = Cart.objects.filter(user=user)
    total_amount = 0
    for item in cart_items:
        total_amount += item.quantity * item.product.discounted_price
    return total_amount


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        carts = Cart.objects.filter(product_id=prod_id, user=request.user)
        
        for cart in carts:
            if cart.quantity > 0:
                cart.quantity -= 1
                cart.save()
        
        total_quantity = sum(cart.quantity for cart in carts)
        total_amount = sum(cart.quantity * cart.product.discounted_price for cart in carts)
        totalamount = calculate_total_amount(request.user)
        
        data = {
            'quantity': total_quantity,
            'amount': total_amount,
            'totalamount': totalamount,
        }
        return redirect("/cart")




def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        Cart.objects.filter(Q(product=prod_id) & Q(user=user)).delete()
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        total_amount = amount + 40
        data = {
            'amount': amount,
            'totalamount': total_amount
        }
    return redirect("/cart")


@login_required
def wishlist(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request, 'wishlist.html', locals())



def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        user = request.user
        wishlist, created = Wishlist.objects.get_or_create(user=user, product=product)
        if created:
            message = "Wishlist Added Successfully"
        else:
            message = "Product already in wishlist"
        return redirect("/product-detail/{0}".format(product.pk))

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        message = "Wishlist Removed Successfully"
        return redirect("/product-detail/{0}".format(product.pk))

@login_required
def search(request):
    query=request.GET['search']
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    product=Product.objects.filter(Q(title__icontains=query))
    return render(request,"search.html",locals())


class CheckoutView(View):
    def get(self, request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)  
        client = Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {
            "amount": razoramount,
            "currency": "INR",
            "receipt": "order_rcptid_12"
        }
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request, "checkout.html", locals())



@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    print("payment_done: oid=", order_id, "pid=", payment_id, "cid=", cust_id)
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=c.product,
            quantity=c.quantity,
            payment=payment
        )
        c.delete()
        # Inserting values into Payment and OrderPlaced models
        payment_data = {
            'user': user,
            'amount': payment.amount,
            'razorpay_order_id': order_id,
            'razorpay_payment_status': payment.razorpay_payment_status
        }
        Payment.objects.create(**payment_data)
        
        order_data = {
            'user': user,
            'customer': customer,
            'product': c.product,
            'quantity': c.quantity,
            'payment': payment
        }
        OrderPlaced.objects.create(**order_data)
        
    cart.delete()  # Delete all cart items for the user
    return redirect("orders")




def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))   

    return render(request,'orders.html',locals())









































