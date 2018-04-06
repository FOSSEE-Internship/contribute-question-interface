from interface.models import (Question, TestCase, StdIOBasedTestCase,
                              AverageRating, Review, QuestionBank
                              )
from yaksh.settings import CODESERVER_HOSTNAME,CODESERVER_PORT
from interface.forms import (RegistrationForm, QuestionForm,
                             SkipForm, ReviewForm
                             )
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.forms.models import inlineformset_factory
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response
from django.template import RequestContext
from urllib.parse import urljoin
import requests
import json
import random


def is_moderator(user):
    """Check if the user is in the moderator group"""
    if user.groups.filter(name='moderator').exists():
        return True

def is_reviewer(user):
    """Check if the user is in the reviewer group"""
    if user.groups.filter(name='reviewer').exists():
        return True

def show_home(request):
    if request.user.is_authenticated():  
        return HttpResponseRedirect(reverse('next_login'))
    else:
        return render(request, 'home.html')
        
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            group = Group.objects.filter(name="reviewer")
            if group.exists():
                user.groups.add(*group)
            messages.add_message(request, messages.SUCCESS,
                                 """<b>You have successfully registered!</b>
                                 You can login now.
                                 """)
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
 
    return render_to_response('register.html', variables)
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))   

@login_required
def next_login(request):
    if request.user.is_authenticated():
        if is_reviewer(request.user):
            return show_review_questions(request)
        return render(request, 'dashboard.html')
    else:
        return render(request, 'home.html')

@login_required
def show_all_questions(request):
    """Show a list of all the questions currently in the database."""

    user = request.user
    context = {}
    if is_reviewer(user) or is_moderator(user):
        return show_review_questions(request)
    if request.method == 'POST':
        if request.POST.get('delete') == 'delete':
            data = request.POST.getlist('question')
            if data is not None:
                questions = Question.objects.filter(id__in=data,
                                                    user_id=user.id
                                                    )
                for question in questions:
                    question.delete()
    questions = Question.objects.filter(user_id=user.id)
    count = questions.count()
    remaining = 5-count
    context['remaining'] = remaining
    context['questions'] = questions
    return render(request, "showquestions.html", context)

@login_required
def add_question(request, question_id=None):
    """Create/edit Questions on the interface"""
    user = request.user
    ci = RequestContext(request)
    if is_reviewer(user):
        return show_review_questions(request)
    test_case_type = "stdiobasedtestcase"
    solution_error, tc_error = [], []

    if Question.objects.filter(user=user).count()>=5 and not question_id:
        return HttpResponseRedirect(reverse('show_all_questions'))
    if question_id is None:
        question = None
    else:
        question = Question.objects.get(id=question_id)
        if not is_moderator(user):
            if question.user != user:
                raise Http404("You cannot access this page")

    if request.method == 'POST':

        qform = QuestionForm(request.POST, instance=question)
        formsets = []
        if qform.is_valid():
            question = qform.save(commit=False)
            question.user = user
            question.save()
            for testcase in TestCase.__subclasses__():
                formset = inlineformset_factory(Question, testcase, extra=0,
                                                fields='__all__')
                formsets.append(formset(
                    request.POST, instance=question
                    )
                )
            for formset in formsets:
                if formset.is_valid():
                    formset.save()
            result = submit_to_code_server(question.id)
            if result.get("success"):
                question.status = True
                question.save()
            else:
                question.status = False
                question.save()
                errors = result.get("error")
                for error in errors:
                    if error.get("type") == "assertion":
                        solution_error.append(error)
                    else:
                        tc_error.append(error)
            test_case_type = request.POST.get('case_type', None)
        else:
            context = {
                'qform': qform,
                'question': question,
                'formsets': formsets,
                "solution_error": solution_error,
                "tc_error": tc_error
            }
            return render_to_response(
                "add_question.html", context, context_instance=ci
            )

    qform = QuestionForm(instance=question)
    formsets = []
    for testcase in TestCase.__subclasses__():
        if test_case_type == testcase.__name__.lower():
            formset = inlineformset_factory(
                Question, testcase, extra=1, fields='__all__'
            )
        else:
            formset = inlineformset_factory(
                Question, testcase, extra=0, fields='__all__'
            )
        formsets.append(
            formset(
                instance=question,
                initial=[{'type': test_case_type}]
            )
        )
    context = {'qform': qform, 'question': question,
               'formsets': formsets, "solution_error":solution_error,
               "tc_error": tc_error}

    return render_to_response(
        "add_question.html", context, context_instance=ci
    )

def submit_to_code_server(question_id, solution=None):
    """Check if question solution and testcases are correct."""

    question = Question.objects.get(id=question_id)
    if solution:
        consolidate_answer = question.consolidate_answer_data(solution)
    else:
        consolidate_answer = question.consolidate_answer_data(
                                      question.solution
                                      )
    url = "http://{0}:{1}".format(CODESERVER_HOSTNAME, CODESERVER_PORT)
    uid = "fellowship" + str(question_id)
    status = False
    requests.post(url, data=dict(uid=uid, json_data=consolidate_answer,
                                 user_dir=""
                                 )
                  )
    while not status:
        result_state = get_result(url, uid)
        stat = result_state.get("status") 
        if stat == "done":
            status = True
            result = json.loads(result_state.get('result'))
            return result
                

def get_result(url, uid):
    response = json.loads(requests.get(urljoin(url, uid)).text)
    return response


@login_required
def show_review_questions(request):
    user = request.user
    context = {}
    if is_moderator(user):
        context['questions'] = Question.objects.filter(status=True)
        status = "moderator"
    if is_reviewer(user):
        ques_bank,created = QuestionBank.objects.get_or_create(user=user)
        questions = get_reviewer_questions(user, ques_bank)
        ques_bank.question_bank.add(*questions)
        context['questions'] = ques_bank.question_bank.all()
        status = "reviewer"
    context['status'] = status
    return render_to_response(
        "show_review_questions.html", context
        )


def get_reviewer_questions(user, question_bank):
    existing_questions = question_bank.question_bank\
                                      .values_list("id", flat=True)
    questions = list(Question.objects.all().exclude(
                                                Q(user=user)
                                                | Q(status=False)
                                                | Q(id__in=existing_questions)
                                                )
                     )
    random.shuffle(questions)
    return questions[:(9-question_bank.question_bank.count())]


@login_required
def check_question(request, question_id):
    """Review question on the interface."""

    user = request.user
    context = {}
    if not is_reviewer(user) and not is_moderator(user):
        raise Http404("You are not allowed to view this page.")

    try:
        question = Question.objects.get(id=question_id)
        review, created = question.reviews.get_or_create(reviewer=user)
    except Question.DoesNotExist:
        raise Http404("The Question you are trying to review doesn't exist.")
    except Review.MultipleObjectsReturned:
        review = question.reviews.filter(reviewer=user).order_by("id").last()

    if request.method == 'POST' and 'check' in request.POST:
        if request.POST.get('answer'):
            answer = request.POST.get('answer')
            review.last_answer = answer
            review.save()
            result = submit_to_code_server(question_id, answer)
            if not result.get("success"):
                context["result"] = result.get("error")
            elif result.get("success"):
                return redirect("/postreview/submit/{0}".format(question.id))
    elif request.method == 'POST' and 'skip' in request.POST:
        return redirect("/postreview/skip/{0}".format(question.id))

    context['question'] = question
    context['last_answer'] = review.last_answer
    return render(request, "checkquestion.html", context)

@login_required
def post_review(request, submit, question_id):
    user = request.user
    context = {}
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("The Question you are trying to review doesn't exist.")
    review = question.reviews.filter(reviewer=user).order_by("id").last()
    if submit=="skip":
        rform = SkipForm(instance=review)
        if request.method == 'POST':
            qform = SkipForm(request.POST, instance=review)
            if qform.is_valid():
                qform.save()
                messages.add_message(request, messages.SUCCESS,
                                    """Your review has been
                                       successfully submitted.
                                    """
                                    )
                return redirect("/dashboard")
    else:
        rform = ReviewForm(instance=review)
        if request.method == 'POST':
            qform = ReviewForm(request.POST, instance=review)
            if qform.is_valid():
                qform.save()
                messages.add_message(request, messages.SUCCESS,
                                    """Your review has been
                                       successfully submitted.
                                    """
                                    )
                return redirect("/dashboard")
    context["rform"] = rform
    return render(request, "skipquestion.html", context)
