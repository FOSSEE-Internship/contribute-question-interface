from django.contrib import admin
from interface.models import (Question, TestCase, StdIOBasedTestCase,
							  Rating, Review)

admin.site.register( Question)
admin.site.register( TestCase)
admin.site.register( Rating)
admin.site.register( Review) 
