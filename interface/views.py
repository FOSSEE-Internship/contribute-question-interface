from interface.models import Question, MultipleChoiceQuestion, CodeQuestion, Choice, TestCase, Rating, Review, Input, Output
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from forms import *
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
from random import choice

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
	
def show_questions_stu(request):
	if request.user.is_authenticated():
		groups = request.user.groups.values_list('name', flat=True)
		if ('admin' in groups or 'moderator' in groups):   
			return HttpResponseRedirect(reverse('next_login'))
		else:                 
			questions = Question.objects.all()
			context = {
				"questions" : questions,
			          }
			return render(request, "display_questions.html", context)
	else:
		return HttpResponseRedirect(reverse('login'))

def show_questions_mod_mcq(request):

	if request.user.is_authenticated():

		groups = request.user.groups.values_list('name', flat=True)
		if ('admin' in groups or 'moderator' in groups):   
			questions = MultipleChoiceQuestion.objects.filter(status=0).order_by('-avg_rating')
			context = {
				"title" : "Unapproved Multiple Choice Questions",
				"questions" : questions,
			          }
			return render(request, "display_questions_mod.html", context)
		else:                 
			return HttpResponseRedirect(reverse('next_login'))
	else:
		return HttpResponseRedirect(reverse('login'))

def show_questions_mod_approved_mcq(request):

	if request.user.is_authenticated():
		
		groups = request.user.groups.values_list('name', flat=True)
		if ('admin' in groups or 'moderator' in groups):   
			questions = MultipleChoiceQuestion.objects.filter(status=1).order_by('-avg_rating')
			context = {
				"title" : "Approved Multiple Choice Questions",
				"questions" : questions,
			          }
			return render(request, "display_questions_mod.html", context)
		else:                 
			return HttpResponseRedirect(reverse('next_login'))
	else:
		return HttpResponseRedirect(reverse('login'))

def show_questions_mod_all(request):
	
	if request.user.is_authenticated():
		
		groups = request.user.groups.values_list('name', flat=True)
		if ('admin' in groups or 'moderator' in groups):   
			questions = Question.objects.all().order_by('-avg_rating')
			context = {
				"title" : "All Questions",
				"questions" : questions,
			          }
			return render(request, "display_questions_mod.html", context)
		else:                 
			return HttpResponseRedirect(reverse('next_login'))
	else:
		return HttpResponseRedirect(reverse('login'))

def show_questions_mod_cq(request):

	if request.user.is_authenticated():
		
		groups = request.user.groups.values_list('name', flat=True)
		if ('admin' in groups or 'moderator' in groups):   
			questions = CodeQuestion.objects.filter(status=0).order_by('-avg_rating')
			context = {
				"title" : "Unapproved Code Questions",
				"questions" : questions,
			          }
			return render(request, "display_questions_mod.html", context)
		else:                 
			return HttpResponseRedirect(reverse('next_login'))
	else:
		return HttpResponseRedirect(reverse('login'))

def show_questions_mod_approved_cq(request):

	if request.user.is_authenticated():
		
		groups = request.user.groups.values_list('name', flat=True)
		if ('admin' in groups or 'moderator' in groups):   
			questions = CodeQuestion.objects.filter(status=1).order_by('-avg_rating')
			context = {
				"title" : "Approved Code Questions",
				"questions" : questions,
			          }
			return render(request, "display_questions_mod.html", context)
		else:                 
			return HttpResponseRedirect(reverse('next_login'))
	else:
		return HttpResponseRedirect(reverse('login'))


def base(request):

	return render(request,'navigation.html')

def add_mcquestion(request):

	if request.user.is_authenticated():
		groups = request.user.groups.values_list('name', flat=True)
		if ('admin' in groups or 'moderator' in groups):   
			return HttpResponseRedirect(reverse('next_login'))
		if request.POST:
			form = MultipleChoiceQuestionForm(request.POST)
			if form.is_valid():
				instance = form.save()
				instance.user=request.user
				instance.save()
			else:
				return render(request, "add_mcquestion.html", {"form": form })

			no_of_inputs = request.POST.get('no_of_inputs')
			
			for i in range(1, int(no_of_inputs)+1):
				choice_text = request.POST.get('choice'+ str(i))
				choice_correct = request.POST.get('correct'+ str(i))
				if (choice_correct==None):
						choice_correct = False
				new_choice = Choice(text=choice_text, question=instance, correct=choice_correct);
				new_choice.save()
	    
			return HttpResponseRedirect(reverse('add_cq'))
		else:
			form = MultipleChoiceQuestionForm()
			return render(request, "add_mcquestion.html", {"form": form })
	else:
		return HttpResponseRedirect(reverse('login'))

def add_cquestion(request):

	if request.user.is_authenticated():
		if request.POST:
			groups = request.user.groups.values_list('name', flat=True)
			if ('admin' in groups or 'moderator' in groups):   
				return HttpResponseRedirect(reverse('mod_show'))
			form = CodeQuestionForm(request.POST)
			if form.is_valid():
				instance = form.save()
				instance.user = request.user
				instance.save()
			else:
				return render(request, "add_cquestion.html", {"form": form }) 
			no_of_testcases = request.POST.get('no_of_testcases')

			inputs = request.POST.get('no_of_inputs')
			outputs = request.POST.get('no_of_outputs')
			for i in range(1, int(no_of_testcases)+1):
				testcase = TestCase(no_of_inputs=inputs, no_of_outputs=outputs, question=instance)
				testcase.save()
				for j in range(1,int(inputs)+1):
					ts_type = request.POST.get('testcase'+str(i)+'_input_'+str(j)+'_type')
					ts_value = request.POST.get('testcase'+str(i)+'_input_'+str(j)+'_value')
					input_instance = Input(_type=ts_type, value=ts_value, test_cases=testcase)
					input_instance.save()

				for j in range(1,int(outputs)+1):
					ts_type = request.POST.get('testcase'+str(i)+'_output_'+str(j)+'_type')
					ts_value = request.POST.get('testcase'+str(i)+'_output_'+str(j)+'_value')
					output_instance =Output(_type=ts_type, value=ts_value, test_cases=testcase)
					output_instance.save()

			return render(request,'notice.html',{'notice':"Thank you for your contribution."})
		else:
			form = CodeQuestionForm()
			return render(request, "add_cquestion.html", {"form": form})
	else:
		return HttpResponseRedirect(reverse('login'))

def next_login(request):

	if request.user.is_authenticated():
		groups = request.user.groups.values_list('name', flat=True)
		if ('admin' in groups or 'moderator' in groups): 
			return render(request, 'dashboard.html', {'type':'moderator', "name":request.user})
		else:
			return render(request, 'dashboard.html', {'type':'user', "name":request.user})
	else:
		return render(request, 'home.html', {'type':'guest'})


def approve_questions(request,id=None):

	question = get_object_or_404(Question,pk=id)
	questions = Question.objects.filter(id=id) 
	ratings_empty = True
	reviews_empty = True
	result_set = []	
	for ques in questions:
		ratings = Rating.objects.filter(question=ques)
		question_dict = {
			"Question" : ques,
			"Ratings" : ratings,
		                }
		result_set.append(question_dict)
		if (ratings):
			ratings_empty = False
	questions = Question.objects.filter(id=id)

	result_set2 = []	
	for ques in questions:
		reviews = Review.objects.filter(question=ques)
		question_dict = {
			"Question" : ques,
			"Reviews" : reviews}
		result_set2.append(question_dict)
		if (reviews):
			reviews_empty=False

	questions = MultipleChoiceQuestion.objects.filter(id=id)
	result_set3 = []
	for ques in questions: 
		choices = Choice.objects.filter(question=ques)
		question_dict = {
			"Question" : ques,
			"Choices" : choices,
		                }
		result_set3.append(question_dict)

	questions = CodeQuestion.objects.filter(id=id)
 	result_set4 = []
	for ques in questions:
		testcases = TestCase.objects.filter(question=ques)
		each_test = []
		for each_testcase in testcases:
			inputs = Input.objects.filter(test_cases=each_testcase)
			outputs = Output.objects.filter(test_cases=each_testcase)
			testcase = {
				"input":inputs,
				"output":outputs,
				 }
			each_test.append(testcase)
		question_dict = {
		"Question" : ques,
		"Testcases" : each_test,
		}
		
		result_set4.append(question_dict)
	context = {
		
		"question_ratings" : result_set,
		"question_reviews" : result_set2,
		"question_choices" : result_set3,
		"question_testcases" : result_set4,
		'question' : question,
		'ratings_empty':ratings_empty,
		'reviews_empty':reviews_empty,
	  		  }

	return render(request, "moderator.html", context)

def approve_questions_accept(request,id=None):

	question = get_object_or_404(Question,pk=id)
	if question.status==1:
		question.status=0
	else:
		question.approve()
	question.save()
	return HttpResponseRedirect("../")	

def show_reviews(request):	

	questions = Question.objects.all()
	result_set = []	
	for ques in questions:
		reviews = Review.objects.filter(question=ques)
		question_dict = {
			"Question" : ques,
			"Reviews" : reviews,
		                }
		result_set.append(question_dict)
	context = {
		"question_reviews" : result_set,
	          }
	return render(request, "display_review.html", context)
	
def show_ratings(request):

	questions = Question.objects.all()
	result_set = []	
	for ques in questions:
		ratings = Rating.objects.filter(question=ques)
		question_dict = {
			"Question" : ques,
			"Ratings" : ratings,
		                }
		result_set.append(question_dict)
	context = { 
		"question_ratings" : result_set,
	          }

	return render(request, "display_rating.html", context)

def add_comment(request,id):
	
	question = get_object_or_404(Question,pk=id)
	questions = Question.objects.filter(id=id)
	ratings_empty=True
	reviews_empty=True
	result_set = []	
	for ques in questions:
		reviews = Review.objects.filter(question=ques)
		question_dict = {
			"Question" : ques,
			"Reviews" : reviews,
		                }
		result_set.append(question_dict)
		if (reviews):
			reviews_empty=False

	questions = Question.objects.filter(id=id)
	result_set2 = []	
	for ques in questions:
		ratings = Rating.objects.filter(question=ques)
		question_dict = {
			"Question" : ques,
			"Ratings" : ratings,
		                }
		result_set2.append(question_dict)
		if (ratings):
			ratings_empty=False
	questions = MultipleChoiceQuestion.objects.filter(id=id)
	result_set3 = []
	for ques in questions: 
		choices = Choice.objects.filter(question=ques)
		question_dict = {
			"Question" : ques,
			"Choices" : choices,
		                }
		result_set3.append(question_dict)

	questions = CodeQuestion.objects.filter(id=id)
 	result_set4 = []
	for ques in questions:
		testcases = TestCase.objects.filter(question=ques)
		each_test = []
		for each_testcase in testcases:
			inputs = Input.objects.filter(test_cases=each_testcase)
			outputs = Output.objects.filter(test_cases=each_testcase)
			testcase = {
				"input":inputs,
				"output":outputs,
				 }
			each_test.append(testcase)
		question_dict = {
		"Question" : ques,
		"Testcases" : each_test,
		}
		
		result_set4.append(question_dict)
	
	context = { 

		"question_reviews" : result_set,
		"question_ratings" : result_set2,
		"question_choices" : result_set3,
		"question_testcases" : result_set4,
		'question' : question ,
		'ratings_empty':ratings_empty,
		'reviews_empty':reviews_empty,
	 		       }


	return render(request,'student.html', context)

def post_comment(request,id):

	if request.POST and request.user.is_authenticated():
		comment = request.POST.get("content")
		rating = request.POST.get("rating")
		user_type=request.POST.get("type")
		rate_type=request.POST.get("rate_type")
		user=request.user.id
		question = get_object_or_404(Question,pk=id)
		if (user_type=='moderator'):
			instance = Review(reviewer_id=user, question=question, comments=comment)
			instance.save()
			return HttpResponseRedirect("../")
		try:
			instance = get_object_or_404(Review, reviewer=user, question=id)
			return render(request,'notice.html',{'notice':"<b>Sorry !</b> You have already commented on this question.<br /><a href=\"../\" >Go back</a>"})
			
		except Exception, e:
			try:
				instance = get_object_or_404(Rating, user=user, question=id)
				return render(request,'notice.html',{'notice':"<b>Sorry !</b> You have already rated this question.<br /> <a href='../'>Go back</a>"})
			except Exception, e:
				
				instance = Rating(user_id=user, question=question, rate=rating)
				instance.save()
				instance = Review(reviewer_id=user, question=question, comments=comment)
				instance.save()
				if (rate_type=='rate_mcq'):
					return HttpResponseRedirect(reverse('rate_cq'))
				elif (rate_type=='rate_cq'):
					return HttpResponseRedirect(reverse('add_mcq'))
				return render(request,'notice.html', {'notice':"<b>Thank you !</b> You have rated this question.<br /> <a href=\"../\" >Go back</a>"})
				

	else:
		return HttpResponseRedirect("../")

def rate_post(request):

	if request.POST and request.user.is_authenticated():
		id = request.POST.get("id")
		comment = request.POST.get("content")
		rating = request.POST.get("rating")
		user_type = request.POST.get("type")
		rate_type = request.POST.get("rate_type")
		user = request.user.id
		try:
			instance = get_object_or_404(Review, reviewer=user,question=id)
			return render(request,'notice.html',{'notice':"<b>Sorry !</b> You have already commented on this question.<br /><a href=\"/\" >Go back</a>"})
			
		except Exception, e:
			try:
				instance = get_object_or_404(Rating, user=user,question=id)
				return render(request,'notice.html',{'notice':"<b>Sorry !</b> You have already rated this question.<br /> <a href='/'>Go back</a>"})
			except Exception, e:
				question = get_object_or_404(Question,pk=id)
				if (user_type!='moderator'):
					instance = Rating(user_id=user,question=question,rate=rating)
					instance.save()

					total_rating = 0
					count = 0
					for rating in Rating.objects.filter(question=question):
						count+=1
						total_rating+=rating.rate
					if (count>0):
						question.avg_rating = (total_rating/count)
					else:
						question.avg_rating = 0
					question.save()

				instance = Review(reviewer_id=user, question=question, comments=comment)
				instance.save()
				if (rate_type=='rate_mcq'):
					return HttpResponseRedirect(reverse('rate_cq'))
				elif (rate_type=='rate_cq'):
					return HttpResponseRedirect(reverse('add_mcq'))
				return render(request,'notice.html',{'notice':"<b>Thank you !</b> You have rated this question.<br /> <a href=\"/\" >Go back</a>"})
				
	else:
		return HttpResponseRedirect("../")
	
def rate_mcq(request):

	if request.user.is_authenticated():
		groups=request.user.groups.values_list('name',flat=True)
		if ('admin' in groups or 'moderator' in groups):   
			return HttpResponseRedirect(reverse('home'))
		else:                 
			questions = MultipleChoiceQuestion.objects.all()
			flag = False
			ratings_empty = True
			reviews_empty = True
			for each in questions:
				try:
					get_object_or_404(Rating,user=request.user,question=each)
				except Exception:
					flag=True
					break
			if flag==True:
				while True:
					random_que = choice(questions)
					try:
						get_object_or_404(Rating, user=request.user, question=random_que)
					except Exception:
						break
				id = random_que.id
				question = get_object_or_404(Question, pk=id)
				questions = Question.objects.filter(id=id)
				result_set = []	
				for ques in questions:
					reviews = Review.objects.filter(question=ques)
					question_dict = {
						"Question" : ques,
						"Reviews" : reviews,
					                }
					if (reviews):
						reviews_empty=False
					result_set.append(question_dict)
				

				questions = Question.objects.filter(id=id)
				result_set2 = []	
				for ques in questions:
					ratings = Rating.objects.filter(question=ques)
					question_dict = {
						"Question" : ques,
						"Ratings" : ratings,
					                }
					if (ratings):
						ratings_empty=False
					result_set2.append(question_dict)

				questions = MultipleChoiceQuestion.objects.filter(id=id)
				result_set3 = []
				for ques in questions: 
					choices = Choice.objects.filter(question=ques)
					question_dict = {
						"Question" : ques,
						"Choices" : choices,
					                }
					result_set3.append(question_dict)

				questions = CodeQuestion.objects.filter(id=id)
			 	result_set4 = []
				for ques in questions:
					testcases = TestCase.objects.filter(question=ques)
					each_test = []
					for each_testcase in testcases:
						inputs = Input.objects.filter(test_cases=each_testcase)
						outputs = Output.objects.filter(test_cases=each_testcase)
						testcase = {
							"input":inputs,
							"output":outputs,
							 }
						each_test.append(testcase)
					question_dict = {
					"Question" : ques,
					"Testcases" : each_test,
					}
					
					result_set4.append(question_dict)
				
				context = { 

					"question_reviews" : result_set,
					"question_ratings" : result_set2,
					"question_choices" : result_set3,
					"question_testcases" : result_set4,
					'question' : question ,
					'rate_type' : 'rate_mcq',
					'ratings_empty':ratings_empty,
					'reviews_empty':reviews_empty,
				 		       }
				
				return render(request,'student.html', context)
			else:
				#return render(request,'notice.html',{'notice':"<b>Thank you !</b> You have already rated all questions.<br /> <a href=\"../ratecq/\" >Next</a>"})
				return HttpResponseRedirect(reverse('rate_cq'))
	else:
		return render(request, 'home.html',{'type':'guest'})

def rate_cq(request):
	
	if request.user.is_authenticated():
		groups = request.user.groups.values_list('name', flat=True)
		if ('admin' in groups or 'moderator' in groups):   
			return HttpResponseRedirect(reverse('home'))
		else:                 
			questions = CodeQuestion.objects.all()
			flag = False;
			ratings_empty = True
			reviews_empty = True
			for each in questions:
				try:
					get_object_or_404(Rating, user=request.user, question=each)
				except Exception:
					flag = True
					break
			if flag==True:
				while True:
					random_que = choice(questions)
					try:
						get_object_or_404(Rating, user=request.user, question=random_que)
					except Exception:
						break
				id = random_que.id
				question = get_object_or_404(Question,pk=id)
				questions = Question.objects.filter(id=id)
				result_set = []	
				for ques in questions:
					reviews = Review.objects.filter(question=ques)
					question_dict = {
						"Question" : ques,
						"Reviews" : reviews,
					                }
					if (reviews):
						reviews_empty=False
					result_set.append(question_dict)
				

				questions = Question.objects.filter(id=id)
				result_set2 = []	
				for ques in questions:
					ratings = Rating.objects.filter(question=ques)
					question_dict = {
						"Question" : ques,
						"Ratings" : ratings,
					                }
					if (ratings):
						ratings_empty=False
					result_set2.append(question_dict)

				questions = MultipleChoiceQuestion.objects.filter(id=id)
				result_set3 = []
				for ques in questions: 
					choices = Choice.objects.filter(question=ques)
					question_dict = {
						"Question" : ques,
						"Choices" : choices,
					                }
					result_set3.append(question_dict)

				questions = CodeQuestion.objects.filter(id=id)
			 	result_set4 = []
				for ques in questions:
					testcases = TestCase.objects.filter(question=ques)
					each_test = []
					for each_testcase in testcases:
						inputs = Input.objects.filter(test_cases=each_testcase)
						outputs = Output.objects.filter(test_cases=each_testcase)
						testcase = {
							"input":inputs,
							"output":outputs,
							 }
						each_test.append(testcase)
					question_dict = {
					"Question" : ques,
					"Testcases" : each_test,
					}
					
					result_set4.append(question_dict)
				
				context = { 

					"question_reviews" : result_set,
					"question_ratings" : result_set2,
					"question_choices" : result_set3,
					"question_testcases" : result_set4,
					'question' : question ,
					'rate_type' : 'rate_cq',
					'ratings_empty':ratings_empty,
					'reviews_empty':reviews_empty,

				 		       }

				return render(request,'student.html', context)
			else:
				#return render(request,'notice.html',{'notice':"<b>Thank you !</b> You have already rated all questions.<br /> <a href=\"../addmcq/\" >next_login</a>"})
				return HttpResponseRedirect(reverse('add_mcq'))
	else:
		return render(request, 'home.html',{'type':'guest'})