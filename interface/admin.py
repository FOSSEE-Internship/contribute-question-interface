from django.contrib import admin, messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import GroupAdmin
from interface.models import Question, TestCase, AverageRating, Review
from interface.views import submit_to_code_server

admin.site.register(Question)
admin.site.register(TestCase)
admin.site.register(AverageRating)
admin.site.register(Review)


class ReviewerAdmin(admin.ModelAdmin):
    search_fields = ['username' ]
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

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'summary']
    list_display = ["summary", "user", 'status']
    actions = ["update_question_status"]

    def update_question_status(self, request, questions):
        try:
            selected_questions = Question.objects.filter(id__in=questions)
            for question in selected_questions:
                result = submit_to_code_server(question.id)
                if result.get("success"):
                    question.status = True
                    question.save()
                else:
                    question.status = False
                    question.save()

            messages.add_message(request, messages.SUCCESS,
                                 "Question Status successfully updated."
                                 )

        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 'You have an error:\n {0}.'.format(e)
                                 )

    update_question_status.short_description = """Check and update
                                                  question status"""


class AverageRatingAdmin(admin.ModelAdmin):
    search_fields = ['question__summary']
    list_display = ["question", "avg_moderator_rating",
                     "avg_peer_rating"
                     ]
    ordering = ["-avg_peer_rating"]
    actions = ["update_ratings"]

    def update_ratings(self, request, questions):
        try:
            selected_questions = Question.objects.filter(id__in=questions)
            for question in selected_questions:
                ratings = AverageRating.objects.get(question=question)
                ratings.set_average_marks()
            messages.add_message(request, messages.SUCCESS,
                                 "Ratings updated."
                                 )

        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 'You have an error:\n {0}.'.format(e)
                                 )

    update_ratings.short_description = """Update marks for
                                                   selected questions
                                                """

admin.site.unregister(User)
admin.site.register(User, ReviewerAdmin)
admin.site.unregister(AverageRating)
admin.site.register(AverageRating, AverageRatingAdmin)
admin.site.unregister(Question)
admin.site.register(Question, QuestionAdmin)
