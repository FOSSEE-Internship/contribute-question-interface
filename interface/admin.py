from django.contrib import admin, messages
from interface.models import (Question, TestCase, StdIOBasedTestCase,
                              Rating, Review)
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import GroupAdmin

admin.site.register(Question)
admin.site.register(TestCase)
admin.site.register(Rating)
admin.site.register(Review)


class ReviewerAdmin(admin.ModelAdmin):
    actions = ['make_reviewer', 'remove_reviewer']

    def make_reviewer(self, request, users):
        try:
            group = Group.objects.get(name="reviewer")
            group.user_set.add(*users)
            messages.add_message(request, messages.SUCCESS,
                                 'Selected users have been added to the group.'
                                 )
        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 'You have an error:\n {0}.'.format(e)
                                 )


    def remove_reviewer(self, request, users):
        try:
            group = Group.objects.get(name="reviewer")
            group.user_set.remove(*users)
            messages.add_message(
                request, messages.SUCCESS,
                'Selected users have been removed from the group.'
                )
        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 'You have an error:\n {0}.'.format(e)
                                 )

    make_reviewer.short_description = "Add Users in reviewer Group"
    remove_reviewer.short_description = "Remove Users from reviewer Group"


admin.site.unregister(User)
admin.site.register(User, ReviewerAdmin)
