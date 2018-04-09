from django import template
from django.template.defaultfilters import stringfilter
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

register = template.Library()

@stringfilter
@register.filter(name='escape_quotes')
def escape_quotes(value):
    if type(value) != str:
        value = value.decode("utf-8")
    escape_single_quotes = value.replace("'", "\\'")
    escape_single_and_double_quotes = escape_single_quotes.replace('"', '\\"')

    return escape_single_and_double_quotes

@register.filter(name='zip')
def zip_longest_out(a, b):
    return zip_longest(a, b)

@register.simple_tag
def get_testcase_error(error_list, expected_output):
    tc_error = None
    success= False
    for error in error_list:
        if expected_output.split("\r\n") == error.get("expected_output"):
            tc_error = error
            success = True
    return {"tc_error":tc_error, "success":success}

@register.simple_tag
def get_review_status(question, user):
    try:
        review_status = question.reviews.get(reviewer=user).status
    except:
        review_status = False
    return review_status
