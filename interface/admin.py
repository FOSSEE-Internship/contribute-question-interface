from django.contrib import admin, messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import GroupAdmin
from django.http import HttpResponse
from interface.models import Question, TestCase, AverageRating, Review
from interface.views import submit_to_code_server, is_moderator

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
    actions = ["update_ratings", "get_unreviewed_questions"]

    def get_unreviewed_questions(self, request, selected_reviews):
        users = User.objects.all()
        qualified = []
        for user in users:
            if not is_moderator(user) \
            and Review.objects.filter(reviewer=user,status=True).count()==10\
             and Question.objects.filter(user=user, status=True).count()==5:
                qualified.append(user)

        question = Question.objects.get(id=475)
        cited_users = []
        for user in qualified:
            try:
                if question.reviews.get(reviewer=user).check_citation == False:
                    cited_users.append(user)
            except:
                pass

        qualified_questions = []
        for user in cited_users:
            qualified_questions.extend(
                Question.objects.filter(user=user,status=True)
                )

        unreviewed_questions = []
        for question in qualified_questions:
            for review in question.reviews.all():
                if review and is_moderator(review.reviewer):
                    break
            else:
                unreviewed_questions.append(question.id)
        filename = "unreviewed_questions.txt"
        content = str(unreviewed_questions)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response

    def update_ratings(self, request, questions):
        try:
            selected_questions = Question.objects.filter(id__in=questions)
            for question in selected_questions:
                ratings,status = AverageRating.objects.get_or_create(
                                                question=question
                                                )
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
    get_unreviewed_questions.short_description = """Get unreviewed questions
                                                """


admin.site.unregister(User)
admin.site.register(User, ReviewerAdmin)
admin.site.unregister(AverageRating)
admin.site.register(AverageRating, AverageRatingAdmin)
admin.site.unregister(Question)
admin.site.register(Question, QuestionAdmin)
