from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile
from django.db.models import Q
from django.contrib.auth.views import LogoutView
from django.views.generic import DetailView
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Avg

def custom_cake(request):
    return render(request, 'custom_cake/build_cake.html')

class MyLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    edit_mode = request.GET.get('edit') == '1'

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
        'edit_mode': edit_mode,
    }
    return render(request, 'shop/profile.html', context)

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.none()
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'shop/search_results.html', {
        'products': products,
        'query': query,
    })

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.object.reviews.all()
        context['average_rating'] = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        context['reviews'] = reviews
        return context

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
    }
    return render(request, 'shop/product_detail.html', context)


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)

        # Получаем корзину из сессии или создаём новую
        cart = request.session.get('cart', {})

        # Добавляем товар в корзину или увеличиваем количество
        if str(product_id) in cart:
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1

        # Сохраняем корзину обратно в сессию
        request.session['cart'] = cart

        # Перенаправляем пользователя на страницу корзины
        return redirect('shop:cart_detail')

    # Если запрос не POST, перенаправляем обратно на страницу товара
    return redirect('shop:product_detail', pk=product_id)

def cart_detail(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart.get(str(product.id), 0)
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'shop/cart_detail.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()

    # Фильтрация по весу (если указана)
    weight = request.GET.get('weight')
    if weight:
        try:
            weight_val = float(weight)
            # Используйте диапазон для сравнения, например ±0.1 для учета округлений
            products = products.filter(weight=weight_val)
        except ValueError:
            pass  # если вес введен некорректно — игнорируем фильтр

    # Сортировка
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    context = {
        'category': category,
        'products': products,
        'current_sort': sort,
    }
    return render(request, 'shop/category_detail.html', context)

def product_list(request):
    products = Product.objects.all()

    weight = request.GET.get('weight')
    if weight:
        try:
            weight_value = float(weight)
            products = products.filter(weight__gte=weight_value)  # фильтр по весу >= введённого
        except ValueError:
            pass  # если введено не число — игнорируем фильтр

    return render(request, 'shop/product_list.html', {'products': products})


def base_view(request):
    categories = Category.objects.all()
    return render(request, 'base.html', {'categories': categories})



