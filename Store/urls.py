from django.urls import path,include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm

urlpatterns = [
    path('',views.index,name="index"),
    path('about/',views.about,name="about"),


    path('contact/',views.contact,name="contact"),
    path('contact/success/',views.contact_success_view, name='contact_success'),

    path('category/<slug:val>',views.CategoryView.as_view(),name="category"),
    path('category-title/<val>',views.CategoryTitle.as_view(),name="category-title"),
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name="product-detail"),

    # Cart
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/',views.CheckoutView.as_view(),name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path("orders/",views.orders,name='orders'),

    path('plus_cart/',views.plus_cart, name='plus_cart'),
    path('minus_cart/', views.minus_cart, name='minus_cart'),
    path('remove_cart/', views.remove_cart, name='remove_cart'), 

    path('search/',views.search,name='search'),   

    #Wishlist
    
    path('wishlist', views.wishlist, name='wishlist'),
    path('plus_wishlist', views.plus_wishlist, name='plus_wishlist'),
    path('minus_wishlist', views.minus_wishlist, name='minus_wishlist'),

    
    # Login Authentication
    path('registration/',views.CustomerRegistrationView.as_view(),name="customerregistration"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm), name="login"),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='change_password.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name="updateAddress"),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class='MySetPasswordForm'),name='password_reset_confirm'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('pssword-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header="Shopping Cart"
admin.site.site_title="Shopping Cart"
admin.site.site_index_title="Welcome to New Shopping Cart"
