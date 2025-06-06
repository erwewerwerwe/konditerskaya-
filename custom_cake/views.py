from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CustomCakeOrderForm
from .models import CustomCakeOrder
from cart.models import Cart, CartItem

@login_required
def build_cake(request):
    if request.method == 'POST':
        form = CustomCakeOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            # Обработка полей "Другое"
            for field in ['biscuit', 'cream', 'filling']:
                if getattr(order, field) == 'other':
                    setattr(order, field, form.cleaned_data.get(f'{field}_custom'))

            # Универсальная обработка оформления:
            decoration_value = form.cleaned_data.get('decoration') or []
            # Если оформление пришло как строка (например, из скрытого поля), превращаем в список
            if isinstance(decoration_value, str):
                decoration_list = [d.strip() for d in decoration_value.split(',') if d.strip()]
            else:
                decoration_list = list(decoration_value)

            custom_decoration = form.cleaned_data.get('decoration_custom')
            if custom_decoration:
                custom_decoration = custom_decoration.strip()
                if custom_decoration:
                    decoration_list.append(custom_decoration)

            # Сохраняем оформления как строку с разделителем без пробелов
            order.decoration = ','.join(decoration_list)

            # Рассчитываем цену
            base_price_per_kg = Decimal('1000.00')
            weight = Decimal(str(order.weight))
            order.price = base_price_per_kg * weight

            order.save()

            cart, _ = Cart.objects.get_or_create(user=request.user)

            # Создаём или обновляем элемент корзины
            item, created = CartItem.objects.get_or_create(
                cart=cart,
                custom_cake=order,
                defaults={'price': order.price}
            )
            if not created:
                item.quantity += 1
                item.price = order.price
                item.save()

            return redirect('cart:cart_detail')
    else:
        form = CustomCakeOrderForm()
    return render(request, 'custom_cake/build_cake.html', {'form': form})

def cart_view(request):
    return render(request, 'custom_cake/cart.html')

@login_required
def add_custom_cake_to_cart(request, cake_id):
    cake = get_object_or_404(CustomCakeOrder, id=cake_id, user=request.user)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    base_price_per_kg = Decimal('1000.00')
    weight = Decimal(str(cake.weight))
    calculated_price = base_price_per_kg * weight

    # Обновляем цену кастомного торта, если нужно
    if cake.price != calculated_price:
        cake.price = calculated_price
        cake.save()

    item, created = CartItem.objects.get_or_create(cart=cart, custom_cake=cake, defaults={'price': calculated_price})

    if not created:
        item.quantity += 1
        item.price = calculated_price
        item.save()
    else:
        item.price = calculated_price
        item.save()

    return redirect('cart:cart_detail')
