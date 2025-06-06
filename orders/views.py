from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.models import Cart  # Предполагается, что корзина реализована


@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    # Подсчёт общей суммы через свойство sub_total у CartItem
    cart_total = sum(item.sub_total for item in cart_items)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart_total
            order.delivery_cost = 0 if form.cleaned_data['pickup_method'] == 'pickup' else 600
            order.save()

            for item in cart_items:
                # Определяем цену для OrderItem
                if item.product:
                    price = item.product.price
                    custom_name = None
                elif item.custom_cake:
                    # Цена кастомного торта
                    if hasattr(item.custom_cake, 'price') and item.custom_cake.price is not None:
                        price = item.custom_cake.price
                    elif hasattr(item.custom_cake, 'get_price'):
                        price = item.custom_cake.get_price()
                    else:
                        price = 0
                    custom_name = str(item.custom_cake)
                else:
                    price = 0
                    custom_name = None

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=price,
                    quantity=item.quantity,
                    custom_name=custom_name,
                )

            cart.items.all().delete()
            return redirect('orders:order_detail', order_id=order.id)
    else:
        form = OrderCreateForm()

    delivery_cost = 0
    if request.method == 'POST' and form.is_valid():
        delivery_cost = 0 if form.cleaned_data['pickup_method'] == 'pickup' else 600

    total = cart_total + delivery_cost

    context = {
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'delivery_cost': delivery_cost,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/user_orders.html', {'orders': orders})

@login_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        return redirect('orders:user_orders')  # или куда хотите после удаления
    # Если GET-запрос, можно показать страницу подтверждения или редирект
    return redirect('orders:user_orders')
