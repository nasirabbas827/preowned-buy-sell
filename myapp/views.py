from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm, RegistrationForm
from django.db.models import Q


from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Category, Product

def index(request):
    # Get all categories for the filter
    categories = Category.objects.all()
    
    # Get all products initially (only available ones)
    products_list = Product.objects.filter(status='Available').order_by('-created_at')
    
    # Get search parameters
    query = request.GET.get('query', '')
    selected_category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    # Apply filters if provided
    if query:
        products_list = products_list.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if selected_category:
        products_list = products_list.filter(category_id=selected_category)
    
    if min_price:
        products_list = products_list.filter(price__gte=min_price)
    
    if max_price:
        products_list = products_list.filter(price__lte=max_price)
    
    # Pagination
    paginator = Paginator(products_list, 9)  # Show 9 products per page
    page = request.GET.get('page')

    products = Product.objects.all()
    
    # Get featured products (newest 3 products)
    featured_products = Product.objects.all().order_by('-created_at')[:3]
    
    context = {
        'categories': categories,
        'products': products,
        'featured_products': featured_products,
        'query': query,
        'selected_category': selected_category,
        'min_price': min_price,
        'max_price': max_price,
    }
    
    return render(request, 'index.html', context)

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to the appropriate dashboard based on usertype
            if user.profile.usertype == 'seller':
                return redirect('seller_dashboard')
            elif user.profile.usertype == 'buyer':
                return redirect('buyer_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Fetch usertype and print it in the terminal
                usertype = user.profile.usertype if hasattr(user, 'profile') else None
                print(f"User Logged In: {user.username}, UserType: {usertype}")  # Debugging
                
                # Set usertype in session
                request.session['usertype'] = usertype
                request.session.modified = True  # Ensure session updates

                # Redirect to appropriate dashboard
                if usertype == 'seller':
                    return redirect('seller_dashboard')
                elif usertype == 'buyer':
                    return redirect('buyer_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
def update_profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def view_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'view_profile.html', {'user_profile': user_profile})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('user_login')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Product  # Import Category and Product models

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from .models import Category, Product, Order, Transaction

@login_required
def seller_dashboard(request):
    user = request.user
    
    # Ensure the user's usertype is fetched from the Profile model
    usertype = user.profile.usertype if hasattr(user, 'profile') else None

    # Fetch only the seller's products and orders
    total_categories = Category.objects.count()  # You might want to count only categories the seller has products in
    total_products = Product.objects.filter(seller=user).count()
    total_orders = Order.objects.filter(seller=user).count()

    # Calculate total payment received by the seller
    total_payment_amount = Transaction.objects.filter(order__seller=user).aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'seller_dashboard.html', {
        'user_type': usertype,
        'total_categories': total_categories,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_payment_amount': total_payment_amount,
    })

@login_required
def seller_orders(request):
    order_status = request.GET.get('status', '')  # Get filter value from request
    orders = Order.objects.filter(product__seller=request.user)

    if order_status:
        orders = orders.filter(order_status=order_status)  # Apply status filter

    return render(request, 'seller_orders.html', {'orders': orders, 'selected_status': order_status})


@login_required
def order_transactions(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, seller=request.user)  # Fix here
    transactions = Transaction.objects.filter(order=order)

    return render(request, 'order_transactions.html', {'order': order, 'transactions': transactions})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Order

@login_required
def buyer_dashboard(request):
    usertype = request.user.profile.usertype if hasattr(request.user, 'profile') else None

    # Get all categories for filter options
    categories = Category.objects.all()

    # Fetch products with optional filters
    query = request.GET.get('query', '')
    category_filter = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    location_filter = request.GET.get('location', '')
    condition_filter = request.GET.get('condition', '')

    products = Product.objects.all()

    if query:
        products = products.filter(title__icontains=query)

    if category_filter:
        products = products.filter(category__id=category_filter)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if location_filter:
        products = products.filter(location__icontains=location_filter)

    if condition_filter:
        products = products.filter(condition=condition_filter)

    # Fetch existing orders to check availability
    ordered_products = Order.objects.values_list('product_id', flat=True)

    return render(request, 'buyer_dashboard.html', {
        'user_type': usertype,
        'categories': categories,
        'products': products,
        'ordered_products': ordered_products,  # Pass ordered product IDs to template
        'query': query,
        'category_filter': category_filter,
        'min_price': min_price,
        'max_price': max_price,
        'location_filter': location_filter,
        'condition_filter': condition_filter,
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, Product
from .forms import OrderForm

@login_required
def make_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Ensure product is available
    if product.status != 'Available':
        messages.error(request, "This product is not available for order.")
        return redirect('buyer_dashboard')

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                buyer=request.user,
                product=product,
                seller=product.seller,
                payment_method=form.cleaned_data['payment_method'],
                delivery_address=form.cleaned_data['delivery_address'],
                order_status='Pending',
                payment_status='Unpaid'  # Set default payment status to Unpaid
            )

            # Mark product as "Pending"
            product.status = 'Pending'
            product.save()

            messages.success(request, "Order placed successfully!")
            return redirect('buyer_dashboard')
    else:
        form = OrderForm()

    return render(request, 'buyer/make_order.html', {'form': form, 'product': product})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order, Transaction

@login_required
def order_list(request):
    orders = Order.objects.filter(buyer=request.user).select_related('product', 'seller')
    return render(request, 'buyer/order_list.html', {'orders': orders})



@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)

    if order.order_status == 'Pending' and order.payment_status == 'Unpaid':
        product = order.product
        product.status = 'Available'
        product.save()

        order.delete()
        messages.success(request, "Your order has been canceled, and the product is now available again.")
    else:
        messages.error(request, "You can only cancel pending orders that are unpaid.")

    return redirect('order_list')




@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)

    # Check if already paid
    if order.payment_status == "Paid":
        messages.error(request, "This order has already been paid for.")
        return redirect("order_list")

    # Update Order and Create Transaction Record
    order.payment_status = "Paid"
    order.order_status = "Completed"
    order.save()

    Transaction.objects.create(
        order=order,
        buyer=request.user,
        amount=order.product.price,
        stripe_charge_id=f"Manual-{order.order_id}"
    )

    messages.success(request, "Payment successful! Your order has been completed.")

    return redirect("order_list")




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category
from .forms import CategoryForm

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'categories/add_category.html', {'form': form})

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/edit_category.html', {'form': form, 'category': category})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == "POST":
        category.delete()
        return redirect('category_list')
    return render(request, 'categories/delete_category.html', {'category': category})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm

@login_required
def product_list(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

@login_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Report, Product

@login_required
def report_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Create a report instance
    report = Report.objects.create(
        reported_by=request.user,
        reported_product=product
    )
    
    messages.success(request, "You have successfully reported this product.")
    return redirect('buyer_dashboard')  # Redirect to buyer dashboard or any relevant page
