from django.template import Library
register = Library()

def contains(in_str, in_substr):
    return in_substr in str(in_str)

register.filter('contains', contains)