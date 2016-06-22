from django.contrib import admin
from interface.models import Question, MultipleChoiceQuestion, CodeQuestion, Choice, TestCase, Rating, Review, Input, Output

admin.site.register( Question)
admin.site.register( MultipleChoiceQuestion)
admin.site.register( CodeQuestion)
admin.site.register( Choice)
admin.site.register( TestCase)
admin.site.register( Rating)
admin.site.register( Review)
admin.site.register( Input)
admin.site.register( Output)
 
