import stripe
from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_product(instance):
    """Создаем stripe продукт"""
    title_product = f'{instance.course}' if instance.course else f'{instance.lesson}'
    stripe_product = stripe.Product.create(name=f"{title_product}")
    product = stripe_product.get('id')
    return product


def create_stripe_price(amount, product):
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount*100,
        product=product,
    )
    return price


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
