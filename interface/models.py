from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

language = (
        ("python", "Python"),
        ("bash", "Bash"),
        ("c", "C Language"),
        ("cpp", "C++ Language"),
        ("java", "Java Language"),
        ("scilab", "Scilab"),
    )


question_types = (
        ("mcq", "Multiple Choice"),
        ("mcc", "Multiple Correct Choices"),
        ("code", "Code"),
    )

test_case_types = (
        ("standardtestcase", "Standard Testcase"),
        ("stdoutbasedtestcase", "Stdout Based Testcase"),
        ("mcqtestcase", "MCQ Testcase"),
    )

question_status_choice = (
        (1, "approved"),
        (0, "unseen"),
        (-1, "discarded"),
        )

level = (
		(1, "easy"),
		(2, "medium"),
		(3, "difficult"),
		)

rating_choice = (
        (1, "Poor"),
        (2, "Average"),
        (3, "Good"),
        (4, "Verygood"),
        (5, "Excellent"),
	    )
types = (
		(1, "integer"),
		(2, "float"),
		(3, "string"),
		(4, "boolean"),
		)

class Question(models.Model):
	title = models.CharField(max_length=50, default="")
	text = models.TextField(default="")
	language = models.CharField(max_length=24, choices=language, default='python')
	marks = models.IntegerField(default=0)
	status = models.IntegerField(default=0, choices=question_status_choice)
	user = models.ForeignKey(User,default=0)
	avg_rating=models.IntegerField(default=0)
	
	def __str__(self):
		return  self.text
	
	def approve(self):
		self.status=1
	
	def disapprove(self):
		self.status=0

class MultipleChoiceQuestion(Question):
	no_of_inputs = models.IntegerField(default=4)
	
	def __str__(self):
	    return  self.text
	    
class Choice(models.Model):
    text = models.TextField(default='')
    question = models.ForeignKey(MultipleChoiceQuestion)
    correct = models.BooleanField(default=False)
    
    def __str__(self):
    	return self.text   


class CodeQuestion(Question):
	function_name = models.CharField(max_length=100, default=None)
	
	def __str__(self):
		return str(self.text)

class TestCase(models.Model):
	
	no_of_inputs = models.IntegerField()
	no_of_outputs = models.IntegerField()
	question = models.ForeignKey(CodeQuestion)
	
	
	def __str__(self):
		return str(self.id)
	

class Rating(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	rate = models.IntegerField(default=3, choices=rating_choice)
	
	def __str__(self):	
		return str(self.user)
		
	class Meta:
		unique_together = ('user', 'question',) 

class Review(models.Model):
	reviewer = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	comments = models.CharField(max_length=24, choices=level)
	
	def __str__(self):	
		return str(self.reviewer)
	
	def update_review(self,new_comments):
		self.comments=new_comments
	#class Meta:
	#	unique_together = ('reviewer', 'question',) 



class Input(models.Model):
	_type = models.CharField(max_length=24, choices=types)
	value = models.CharField(max_length=24)
	test_cases = models.ForeignKey('TestCase')
	
	def __str__(self):
		return str(self._type) +"+"+ str(self.value)

class Output(models.Model):
	_type = models.CharField(max_length=24, choices=types)
	value = models.CharField(max_length=24)
	test_cases = models.ForeignKey('TestCase')
	
	def __str__(self):
		return str(self._type) +"+"+ str(self.value)
