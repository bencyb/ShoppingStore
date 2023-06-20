from django.contrib import admin
from . models import Cart,Customer,OrderPlaced,Payment,Product,Wishlist,Contact
from django.contrib.auth.models import Group
# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
	list_display=['id','title','discounted_price','category','product_image']


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
	list_display=['id','user','locality','city','state','zipcode']

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
	list_display=['id','name','email','message','created_at']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
	list_display=['id','user','product','quantity']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
	list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
	list_display=['id','user','customer','product','quantity','ordered_date','status','payment']


@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
	list_display=['id','user','product']

admin.site.unregister(Group)