# cart_context.py

from ecohiveapp.models import Cart  # Import your Cart model

def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_item_count = cart_items.count()
    else:
        cart_item_count = 0

    return {'cart_item_count': cart_item_count}
