from django import template
import math

register = template.Library()

@register.simple_tag
def call_sellprice(price, discount):
    if discount is None or discount is 0:
        return price
    sellprice = price
    sellprice = price - (price * discount/100)
    return math.floor(sellprice)

@register.simple_tag
def progress_bar(total_quantity, availability):
    progress_precent = availability
    progress_precent = availability/total_quantity * 100
    return math.floor(progress_precent)
