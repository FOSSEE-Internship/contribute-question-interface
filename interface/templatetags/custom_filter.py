from django import template
from django.template.defaultfilters import stringfilter
import os
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

register = template.Library()


@register.filter(name='zip')
def zip_longest_out(a, b):
    return zip_longest(a, b)

@register.simple_tag
def get_testcase_error(error_list, expected_output):
	tc_error = None
	for error in error_list:
		if expected_output == error.get("expected_output")[0]:
			tc_error = error
	return tc_error
