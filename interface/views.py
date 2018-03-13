from interface.models import (Question, TestCase, StdIOBasedTestCase,
                              Rating, Review)
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from interface.forms import *
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
from random import choice
from urllib.parse import urljoin
import requests
import json
import os

def show_home(request):  
    
    if request.user.is_authenticated():  
        return HttpResponseRedirect(reverse('next_login'))
    else:
        return render(request, 'home.html', {'type':'guest'})
        
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return render(request,'notice.html',{'notice':"<b>Thank you !</b> Your registration success.<br /> <a href=\"/login\" >Login</a>"})
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
 
    return render_to_response('registration/register.html', variables)

def register_success(request):
    return render_to_response('registration/success.html')
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))   

@login_required
def next_login(request):

    if request.user.is_authenticated():
        groups = request.user.groups.values_list('name', flat=True)
        if ('admin' in groups or 'moderator' in groups): 
            return render(request, 'dashboard.html', {'type':'moderator', "name":request.user})
        else:
            return render(request, 'dashboard.html', {'type':'user', "name":request.user})
    else:
        return render(request, 'home.html', {'type':'guest'})

@login_required
def show_all_questions(request):
    """Show a list of all the questions currently in the database."""

    user = request.user
    ci = RequestContext(request)
    context = {}
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
    context['questions'] = questions
    context['remaining'] = remaining
    return render(request, "showquestions.html", context)

@login_required
def add_question(request, question_id=None):
    user = request.user
    ci = RequestContext(request)
    test_case_type = "stdiobasedtestcase"
    solution_error, tc_error = [], []
    if Question.objects.filter(user=user).count()>=5:
        return HttpResponseRedirect(reverse('show_all_questions'))

    if question_id is None:
        question = None
    else:
        question = Question.objects.get(id=question_id)

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

def submit_to_code_server(question_id):
    """Check if question solution and testcases are correct."""

    question = Question.objects.get(id=question_id)
    consolidate_answer = question.consolidate_answer_data(question.solution)
    url = "http://localhost:55555"
    uid = "fellowship" + str(question_id)
    status = False
    submit = requests.post(url, data=dict(uid=uid, json_data=consolidate_answer, user_dir=""))
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
