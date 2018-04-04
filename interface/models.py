from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import json

question_status_choices = (
        (1, "Question doesn't make sense."),
        (2, "Question makes sense, but is too difficult to solve."),
        (3, "Question is correct, but the test cases are wrong."),
        )

rating_choice = (
        (1, "Poor"),
        (2, "Average"),
        (3, "Good"),
        (4, "Verygood"),
        (5, "Excellent"),
        )

originality = (
        ("original", "Original Question"),
        ("adapted", "Adapted Question"),
        )


class Question(models.Model):
    """Question for a quiz."""

    # A one-line summary of the question.
    summary = models.CharField(max_length=256)

    # The question text, should be valid HTML.
    description = models.TextField()

    # Number of points for the question.
    points = models.FloatField(default=1.0)

    # The language for question.
    language = models.CharField(max_length=24,
                                default="python")

    # The type of question.
    type = models.CharField(max_length=24, default="code")

    # user for particular question
    user = models.ForeignKey(User, related_name="user")

    # solution for question
    solution = models.TextField()

    # If the question is cited
    citation = models.TextField(null=True, blank=True,
                                help_text="Please add appropriate citation\
                                if the question is adapted from elsewhere."
                                )

    # originality of the question
    originality = models.CharField(max_length=24, choices=originality, default="original")

    #status of question
    status = models.BooleanField(default=False)

    def __str__(self):
        return  self.summary
    
    def _get_test_cases(self):
        tc_list = [tc.stdiobasedtestcase for tc in TestCase.objects.filter(question=self)]
        return tc_list

    def consolidate_answer_data(self, user_answer, user=None):
        question_data = {}
        metadata = {}
        test_case_data = []

        test_cases = self._get_test_cases()

        for test in test_cases:
            test_case_as_dict = test.get_field_value()
            test_case_data.append(test_case_as_dict)

        question_data['test_case_data'] = test_case_data
        metadata['user_answer'] = user_answer
        metadata['language'] = self.language
        metadata['partial_grading'] = False
        question_data['metadata'] = metadata
        return json.dumps(question_data)


class TestCase(models.Model):
    question = models.ForeignKey(Question, blank=True, null=True)
    type = models.CharField(max_length=24, default="stdiobasedtestcase")

class StdIOBasedTestCase(TestCase):
    expected_input = models.TextField(default=None, blank=True, null=True)
    expected_output = models.TextField(default=None)

    def get_field_value(self):
        return {"test_case_type": "stdiobasedtestcase",
                "expected_output": self.expected_output,
                "expected_input": self.expected_input,
                "weight": 1
                }

    def __str__(self):
        return u'StdIO Based Testcase | Exp. Output: {0} | Exp. Input: {1}'.\
            format(
                self.expected_output, self.expected_input
            )
    

class Rating(models.Model):
    question = models.ForeignKey(Question)
    avg_moderator_rating = models.FloatField(default=0.0)
    avg_peer_rating = models.FloatField(default=0.0)

    def __str__(self):  
        return "Rating for {0}".format(self.question.summary)
        

class QuestionReviewDetails(models.Model):
    question = models.ForeignKey(Question)
    rating = models.IntegerField(default=3, choices=rating_choice)
    comments = models.TextField(null=True, blank=True)
    check_citation = models.BooleanField(default=False)
    question_status = models.IntegerField(blank=True, null=True,
                                          choices=question_status_choices
                                          )
    skipped = models.BooleanField(default=False)

    def __str__(self):  
        return "Review for {0}".format(self.question.summary)


class Review(models.Model):
    user = models.ForeignKey(User)
    admin_review = models.BooleanField(default=False)
    question_details = models.ManyToManyField(QuestionReviewDetails,
                                              related_name="question_details"
                                              )

class QuestionBank(models.Model):
    user = models.ForeignKey(User)
    question_bank = models.ManyToManyField(Question)
