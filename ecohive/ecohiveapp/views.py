from audioop import reverse
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import User
from .forms import SignUpForm, LoginForm
from .forms import CertificationForm
from django.contrib.auth import authenticate, login
from ecohiveapp.models import User 
from .models import Certification
from django.shortcuts import get_object_or_404

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required 
from .models import Category,Product,Seller,UserProfile
from django.db import IntegrityError  
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
from allauth.account.views import SignupView
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
from .models import Cart


# from .forms import CustomUserCreationForm
  
# Make sure the import path is correct

# Create your views here.


from .models import ProductSummary  # Import your ProductSummary model


def index(request):
    products = Product.objects.all()
    context = {
            'products': products,
        }  # Fetch all ProductSummary instances
    return render(request, 'index.html', context)

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})



def user_login(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                auth_login(request,user)
                if user.is_customer:
                    # login(request, user)
                    request.session['customer_id'] = user.id
                    request.session['user_type'] = 'customer'
                    return redirect('index')
                elif user.is_seller:
                    # login(request, user)
                    request.session['seller_id'] = user.id
                    request.session['user_type'] = 'seller'
                    return redirect('index')
                elif user.is_legaladvisor:
                    print("Redirecting to dashlegal")
                    request.session['legaladvisor_id'] = user.id
                    request.session['user_type'] = 'legaladvisor'
                    return redirect('dashlegal')
                elif user.is_superuser:
                    print("Redirecting to dashlegal")
                    request.session['admin_id'] = user.id
                    request.session['user_type'] = 'admin'
                    return redirect('admindash')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'

    return render(request, 'login.html', {'form': form, 'msg': msg})

@login_required
def dashseller(request):
    existing_certification = Certification.objects.filter(user=request.user).first()

    if existing_certification:
        return render(request, 'dashseller.html', {'existing_certification': existing_certification})

    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")  # Debug statement
            certification = form.save(commit=False)
            certification.user = request.user
            certification.save()
            print("Certification saved successfully")  # Debug statement
            return redirect('successseller')  # Redirect to a success page
        else:
            messages.error(request, 'Please fill in all required fields.')
            # Debug statement
    else:
        form = CertificationForm()

    return render(request, 'dashseller.html', {
        'form': form,
        'existing_certification': existing_certification,
    })


def dashlegal(request):
    # Retrieve Certification objects
    seller_applications = Certification.objects.all()

    # Retrieve User roles for each Certification applicant
    user_roles = {}
    for application in seller_applications:
        # Ensure the user associated with the Certification exists
        user = get_object_or_404(User, id=application.user_id)

        # Retrieve user roles
        user_roles[application.id] = {
            'is_admin': user.is_admin,
            'is_customer': user.is_customer,
            'is_seller': user.is_seller,
            'is_legaladvisor': user.is_legaladvisor,
        }

    context = {
        'seller_applications': seller_applications,
        'user_roles': user_roles,  # Include user roles in the context
    }
    return render(request, 'dashlegal.html', context)


def loggout(request):
    print('Logged Out')
    logout(request)
    if 'username' in request.session:
        del request.session['username']
        request.session.clear()
    return redirect('login')

def check_email(request):
    email = request.GET.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})

def check_username(request):
    username = request.GET.get('username')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

import json

@login_required
def admindash(request):
    # Calculate the total number of users
    total_users = User.objects.count()

    # Calculate the number of products added
    total_products = Product.objects.count()

    # Calculate the number of certified users
    total_certified_users = Certification.objects.filter(is_approved='approved').count()

    # Calculate the total number of orders
    total_orders = Order.objects.count()

    # Prepare data for the chart
    order_labels = ['Total Orders']
    order_data = [total_orders]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_certified_users': total_certified_users,
        'total_orders': total_orders,
        'order_labels': json.dumps(order_labels),  # Convert to JSON format for JavaScript
        'order_data': json.dumps(order_data),      # Convert to JSON format for JavaScript
    }
    return render(request, 'admindash/admindash.html', context)

@login_required
def addcategory(request):
    if request.method == 'POST':
        try:
            # Retrieve form data directly from the request
            category_name = request.POST.get('category_name')
            formatted_category_name = category_name.capitalize()
            category_description = request.POST.get('category_description')

            # Check if the category already exists
            category, created = Category.objects.get_or_create(
                category_name=formatted_category_name,
                defaults={'category_description': category_description}
            )

            if created:
                # The category was created
                messages.success(request, 'Category created successfully.')
            else:
                # The category already exists
                messages.error(request, 'Category already exists.')

            return redirect('successaddcategory')  # Redirect back to the admin page

        except IntegrityError as e:
            # Handle other database integrity errors if needed
            messages.error(request, 'Error creating category: {}'.format(str(e)))

    return render(request, 'admindash/addcategory.html')

def viewcategory(request):
    categories = Category.objects.all()
    return render(request, 'admindash/viewcategory.html', {'categories': categories})

def successseller(request):
    return render(request, 'sellerdash/successseller.html')

def successaddcategory(request):
    return render(request, 'admindash/successaddcategory.html')

def successaddproduct(request):
    return render(request, 'sellerdash/successaddproduct.html')

@login_required
def viewaddproduct(request):
    existing_certification = Certification.objects.filter(user=request.user).first()

    seller_instance = Seller.objects.get(user=request.user)
    if not existing_certification:
        messages.error(request, 'You need an approved certification to add products.')
        return redirect('dashseller')
        # Query the Product model to retrieve products associated with the current user's Seller instance
    user_products = Product.objects.filter(seller=seller_instance)

    # Your other view logic goes here...

    return render(request, 'sellerdash/viewaddproduct.html', {'user_products': user_products})

@login_required
def viewproducts(request):
    # Retrieve all products
    all_products = Product.objects.all()

    context = {
        'all_products': all_products,
    }
    return render(request, 'admindash/viewproducts.html', context)

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Handle form submission for deleting the product
        product.delete()
        return redirect('viewproducts')

    # Render the delete product template
    return render(request, 'admindash/delete_product.html', {'product': product})

@login_required
def addproducts(request):
    existing_certification = Certification.objects.filter(user=request.user).first()

    if existing_certification:
        certification_status = existing_certification.is_approved
    else:
        certification_status = 'pending'  # Set a default value if no certification exists

    if certification_status == 'approved':

        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            formatted_product_name = product_name.capitalize()
            product_description = request.POST.get('product_description')
            select_category_id = request.POST.get('select_category')
            product_price = request.POST.get('product_price')
            product_stock = request.POST.get('product_stock')
            product_image = request.FILES.get('product_image')

        # Retrieve the selected category
            category = Category.objects.get(id=select_category_id)

        # Check if a product with the same name already exists in the selected category
        # Check if the current user has already added a product with the same name in this category
            existing_product = Product.objects.filter(
                product_name=formatted_product_name,
                category=category,
                seller__user=request.user  # Filter by the current user
            )

            if existing_product.exists():
                error_message = "You have already added a product with this name in the selected category."
                return render(request, 'sellerdash/addproducts.html', {'error_message': error_message})

        # Retrieve the seller associated with the currently logged-in user
            seller = Seller.objects.get(user=request.user)

        # Create and save the Product instance
            product = Product(
                product_name=formatted_product_name,
                product_description=product_description,
                category=category,
                product_price=product_price,
                product_stock=product_stock,
                product_image=product_image,
                seller=seller  # Associate the seller with the product
            )
            product.save()

            return redirect('successaddproduct')  # Redirect to a success page or your desired destination

        categories = Category.objects.all()  # Retrieve all Category objects from the database

        context = {
        'categories': categories,
        'certification_status': certification_status,
  # Pass the categories queryset to the template context
         }
        return render(request, 'sellerdash/addproducts.html', context)
    else:
        return render(request, 'sellerdash/addproducts.html', {'certification_status': certification_status})

def delete_category(request, category_id):
    # Get the category object to delete
    category = get_object_or_404(Category, pk=category_id)

    associated_products = Product.objects.filter(category=category)

    if request.method == 'POST':
        # Delete all associated products
        associated_products.delete()
        
        # Delete the category
        category.delete()
        
        return redirect('viewcategory')  # Redirect to the category list page

    return render(request, 'admindash/delete_category.html', {'category': category, 'associated_products': associated_products})

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        new_category_name = request.POST['category_name']
        
        # Check if a category with the same name already exists
        if Category.objects.filter(category_name=new_category_name).exclude(id=category.id).exists():
            messages.error(request, 'Category with this name already exists.')
        else:
            # Update the category if no duplicate name found
            category.category_name = new_category_name
            category.category_description = request.POST['category_description']
            category.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('viewcategory')  # Replace 'category_list' with your category list URL name

    return render(request, 'admindash/edit_category.html', {'category': category})

def delete_certification(request, certification_id):
    certification = get_object_or_404(Certification, id=certification_id)
    certification.delete()
    return redirect('dashlegal')

#USER DASHBOARD
@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If UserProfile doesn't exist, create one for the user
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            user_profile.profile_pic = profile_pic

        user_profile.name = name
        user_profile.phone_number = phone_number
        user_profile.address = address
        request.user.email = email

        user_profile.save()
        request.user.save()
        # messages.success(request, "Profile updated successfully")
        return redirect('profile')
    
    return render(request, 'userprofile/user_profile.html', {'user_profile': user_profile})



def user_dashboard(request):
    return render(request,'userprofile/user_dashboard.html')

def user_list(request):
    users = User.objects.all()

    if request.method == 'POST':
        # Handle form submission and update user details
        user_id = request.POST['user_id']
        user = get_object_or_404(User, id=user_id)

        user.username = request.POST['username']
        user.email = request.POST['email']

        role = request.POST.get('role')

        if role == 'customer':
            user.is_customer = True
            user.is_seller = False
            user.is_admin = False
            user.is_legaladvisor = False
        elif role == 'seller':
            user.is_customer = False
            user.is_seller = True
            user.is_admin = False
            user.is_legaladvisor = False
        elif role == 'admin':
            user.is_customer = False
            user.is_seller = False
            user.is_admin = True
            user.is_legaladvisor = False
        elif role == 'legaladvisor':
            user.is_customer = False
            user.is_seller = False
            user.is_admin = False
            user.is_legaladvisor = True
        # Update user status based on the selected status option
        status = request.POST.get('status')
        if status == 'active':
            user.is_active = True
        else:
            user.is_active = False

        user.save()

        # Return a JSON response to indicate a successful update
        return JsonResponse({'success': True})
    
    return render(request, 'admindash/userlist.html', {'users': users})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt  # Use csrf_exempt for simplicity; consider using a csrf token for security in production
def delete_user(request, user_id):
    # Check if the request method is POST (for safety, you might want to use a confirmation modal before sending the request)
    if request.method == 'POST':
        # Get the user object to delete
        user = get_object_or_404(User, id=user_id)

        # Check if the user can be deleted (e.g., you might want to add custom logic here)
        if not user.is_superuser:
            user.delete()
            return JsonResponse({'message': 'User deleted successfully.'})

    return JsonResponse({'error': 'Unable to delete user.'}, status=400)

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Handle form submission and update user details
        user.username = request.POST['username']
        user.email = request.POST['email']

        # Update user role based on the selected role option
        role = request.POST.get('role')
        if role == 'customer':
            user.is_seller = False
            user.is_superuser = False
            user.is_customer = True
        elif role == 'seller':
            user.is_seller = False
            user.is_superuser = False
            user.is_customer = True
        elif role == 'superuser':
            user.is_seller = False
            user.is_superuser = False
            user.is_customer = True
        status = request.POST.get('status')
        if status == 'active':
            user.is_active = True
        elif status == 'inactive':
            user.is_active = False


        user.save()
        return redirect('user_list')  # Redirect back to the user list page

    return render(request, 'admindash/edituser.html', {'user': user})

def approve_certification(request, certification_id):
    certification = get_object_or_404(Certification, id=certification_id)
    if request.method == 'POST':
        certification.is_approved = Certification.APPROVED  # Set it to 'approved'
        certification.save()
    return redirect('dashlegal')

def reject_certification(request, certification_id):
    certification = get_object_or_404(Certification, id=certification_id)
    if request.method == 'POST':
        certification.is_approved = Certification.REJECTED  # Set it to 'rejected'
        certification.save()
    return redirect('dashlegal')

from .models import ProductSummary

def view_products(request):
    product_summaries = ProductSummary.objects.all()
    return render(request, 'admindash/viewstock.html', {'product_summaries': product_summaries})

def edit_product_stock(request, pk):
    product_summary = get_object_or_404(ProductSummary, pk=pk)

    if request.method == 'POST':
        # Handle the form submission and update the product details directly in the model
        product_summary.product_description = request.POST['product_description']
        product_summary.product_price = request.POST['product_price']
        product_summary.product_image = request.FILES['product_image']
        product_summary.save()
        return redirect('viewstock')  # Redirect to the product summary page after editing

    return render(request, 'admindash/editstock.html', {'product_summary': product_summary})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        new_product_name = request.POST['product_name']

        # Check if a product with the same name already exists (excluding the current product)
        if Product.objects.filter(product_name=new_product_name).exclude(id=product.id).exists():
            messages.error(request, 'A product with this name already exists.')
        else:
            # Update the product fields based on form input
            product.product_name = new_product_name
            product.product_description = request.POST['product_description']

            category_id = request.POST.get('select_category')
            if category_id:
                category = get_object_or_404(Category, id=category_id)
                product.category = category

            product.product_price = request.POST['product_price']
            product.product_stock = request.POST['product_stock']

            if 'product_image' in request.FILES:
                product.product_image = request.FILES['product_image']

            product.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('viewaddproduct')

    return render(request, 'sellerdash/edit_product.html', {'product': product, 'categories': categories})

def delete_add_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Handle form submission for deleting the product
        product.delete()
        return redirect('viewaddproduct')  # Redirect to the product list page

    return render(request, 'sellerdash/delete_add_product.html', {'product': product})

def wishlist(request):
    # Add your logic here
    return render(request, 'wishlist.html')


@login_required
def product_single(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user

    # Check if the product is already in the user's cart
    existing_cart_item = Cart.objects.filter(user=user, product=product).first()
    is_in_cart = existing_cart_item is not None

    # Include the product stock in the context
    context = {
        'product': product,
        'is_in_cart': is_in_cart,
        'product_stock': product.product_stock,  # Pass the product stock to the template
    }

    if request.method == 'POST':
        # If it's a POST request, get the quantity from the form
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided
        image = product.product_image

        if not is_in_cart:
            # If the product is not in the cart, add it to the cart with the specified quantity
            Cart.objects.create(user=user, product=product, quantity=quantity, image=image)
        else:
            # If the product is already in the cart, update the quantity
            existing_cart_item.quantity += quantity
            existing_cart_item.save()

        return redirect('cart')  # Redirect to the cart page or any other page you prefer

    return render(request, 'product-single.html', context)



def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)

    if request.method == 'POST':
        cart_item.delete()

    return redirect('cart')

def update_cart_item(request, cart_item_id):
    if request.method == 'POST':
        # Retrieve the cart item
        cart_item = Cart.objects.get(id=cart_item_id)

        # Get the new quantity from the form
        new_quantity = int(request.POST.get('quantity'))

        # Update the cart item's quantity
        cart_item.quantity = new_quantity
        cart_item.save()

    # Redirect back to the cart view
    return redirect('cart')
  

def about(request):
    # Add your logic here
    return render(request, 'about.html')
def shop(request):
    products = Product.objects.all()
    
    return render(request, 'shop.html', {'products': products})

def category_vegetables(request):
    # Filter products by the "Vegetables" category
    vegetables_category = Category.objects.get(category_name='Vegetables')
    vegetable_products = Product.objects.filter(category=vegetables_category)

    # Pass the filtered products to the template
    context = {
        'category_products': {'Vegetables': vegetable_products},
    }

    return render(request, 'category_vegetables.html', context)

def category_fruits(request):
    fruits_category = Category.objects.get(category_name='Fruits')
    fruit_products = Product.objects.filter(category=fruits_category)

    # Pass the filtered products to the template
    context = {
        'category_products': {'Fruits': fruit_products},
    }

    return render(request, 'category_fruits.html', context)


    
def paymentsuccess(request):
    # Add your logic here
    return render(request, 'paymentsuccess.html')


def cart_view(request):
    # Assuming you have user authentication and each user has a unique cart
    user = request.user

    # Retrieve the user's cart items
    cart_items = Cart.objects.filter(user=user)

    # Calculate the total price of items in the cart
    total_price = sum(cart_item.product.product_price * cart_item.quantity for cart_item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)

from .models import BillingDetails, Cart, Order  # Import your models here
from django.shortcuts import render, redirect
from decimal import Decimal

from django.db import transaction

@transaction.atomic
def checkout(request):
    total_price = 0  # Initialize total_price outside the if block
    cart_items = Cart.objects.filter(user=request.user)  # Define cart_items here
    billing_details = None  # Initialize billing_details to None

    # Check if billing details exist for the user
    if BillingDetails.objects.filter(user=request.user).exists():
        billing_details = BillingDetails.objects.get(user=request.user)

    if request.method == 'POST' and 'place_order' in request.POST:
        # If billing details already exist, you can skip processing the form and just calculate the total price
        if not billing_details:
            # Retrieve and process the form data for billing details
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            state = request.POST.get('state')
            street_address = request.POST.get('streetaddress')
            apartment_suite_unit = request.POST.get('apartmentsuiteunit')
            town_city = request.POST.get('towncity')
            postcode_zip = request.POST.get('postcodezip')
            phone = request.POST.get('phone')
            email = request.POST.get('emailaddress')

            # Create BillingDetails object (assuming BillingDetails is a separate model)
            billing_details = BillingDetails(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                state=state,
                street_address=street_address,
                apartment_suite_unit=apartment_suite_unit,
                town_city=town_city,
                postcode_zip=postcode_zip,
                phone=phone,
                email=email,
            )
            billing_details.save()

        total_price = sum(item.product.product_price * item.quantity for item in cart_items)

        # Convert total_price to a float before storing it in the session
        request.session['order_total'] = float(total_price)

        # Redirect to the payment page to complete the order
        return redirect('payment')

    # If it's not a POST request or not a place order request, continue displaying the cart items
    total_price = sum(item.product.product_price * item.quantity for item in cart_items)

    # Convert total_price to a float before passing it to the template
    context = {
        'cart_items': cart_items,
        'total_price': float(total_price),
        'billing_details': billing_details,  # Pass billing_details to the template
    }

    return render(request, 'checkout.html', context)


#payment
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def payment(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = Decimal(sum(cart_item.product.product_price * cart_item.quantity for cart_item in cart_items))
    
    currency = 'INR'

    # Set the 'amount' variable to 'total_price'
    amount = int(total_price*100)
    # amount=20000

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # Order id of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        razorpay_order_id=razorpay_order_id,
        payment_status=Order.PaymentStatusChoices.PENDING,
    )

    # Add the products to the order
    for cart_item in cart_items:
        order.products.add(cart_item.product)

    # Save the order to generate an order ID
    order.save()

    # Create a context dictionary with all the variables you want to pass to the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'payment.html', context=context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        # Verify the payment signature.
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        result = razorpay_client.utility.verify_payment_signature(params_dict)

        if not result:
            # Signature verification failed.
            return render(request, 'paymentfail.html')

        # Signature verification succeeded.
        # Retrieve the order from the database
        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        except Order.DoesNotExist:
            return HttpResponseBadRequest("Order not found")

        if order.payment_status == Order.PaymentStatusChoices.SUCCESSFUL:
            # Payment is already marked as successful, ignore this request.
            return HttpResponse("Payment is already successful")

        if order.payment_status != Order.PaymentStatusChoices.PENDING:
            # Order is not in a pending state, do not proceed with stock update.
            return HttpResponseBadRequest("Invalid order status")

        # Capture the payment amount
        amount = int(order.total_price * 100)  # Convert Decimal to paise
        razorpay_client.payment.capture(payment_id, amount)

        # Update the order with payment ID and change status to "Successful"
        order.payment_id = payment_id
        order.payment_status = Order.PaymentStatusChoices.SUCCESSFUL
        order.save()

        # Remove the products from the cart and update stock
        cart_items = Cart.objects.filter(user=request.user)
        for cart_item in cart_items:
            product = cart_item.product
            if product.product_stock >= cart_item.quantity:
                # Decrease the product stock and update ProductSummary
                product.product_stock -= cart_item.quantity
                product.save()
                summary, created = ProductSummary.objects.get_or_create(product_name=product.product_name)
                summary.update_total_stock()
                # Remove the item from the cart
                cart_item.delete()
            else:
                # Handle insufficient stock, you can redirect or show an error message
                return HttpResponseBadRequest("Insufficient stock for some items")

        # Redirect to a payment success page
        return redirect('orders')

    return HttpResponseBadRequest("Invalid request method")


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)

    context = {
        'orders': orders,
    }

    return render(request, 'orders.html', context)

def view_orders(request):
    all_orders = Order.objects.all()

    return render(request, 'admindash/view_orders.html', {'all_orders': all_orders})