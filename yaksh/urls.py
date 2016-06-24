from django.conf.urls import url, include
from django.contrib import admin
from interface.views import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',"interface.views.show_home",name="home"),

    url(r'^login/$', 'django.contrib.auth.views.login', name="login"), 
    url(r'^logout/$', "interface.views.logout_page",name="logout_page"), 
    url(r'^register/$', "interface.views.register", name="register_page"),
    url(r'^register/success/$', "interface.views.register_success",name="register_success"),    
    url(r'^dashboard/$',"interface.views.next_login",name="next_login"),

    url(r'^questions/$',"interface.views.show_questions_stu",name="stu_questions"),
    url(r'^questions/ratemcq/$',"interface.views.rate_mcq",name="rate_mcq"),
    url(r'^questions/postcomment/$',"interface.views.rate_post",name="rate_post_comment"),
    url(r'^questions/ratecq/$',"interface.views.rate_cq",name="rate_cq"),
    url(r'^questions/addmcq/$',"interface.views.add_mcquestion",name="add_mcq"),  
    url(r'^questions/addcq/$',"interface.views.add_cquestion",name="add_cq"),  

    url(r'^questions/(?P<id>\d+)/$',"interface.views.add_comment",name="question_comment"),
    url(r'^questions/(?P<id>\d+)/postcomment/$',"interface.views.post_comment",name="question_comment_post"),

    url(r'^moderator/$',"interface.views.next_login",name="mod_show"),
    url(r'^moderator/all/$',"interface.views.show_questions_mod_all",name="mod_show_all"),
    url(r'^moderator/mcq/$',"interface.views.show_questions_mod_mcq",name="mod_show_mcq"),
    url(r'^moderator/cq/$',"interface.views.show_questions_mod_cq",name="mod_show_cq"),
    url(r'^moderator/mcq_approved/$',"interface.views.show_questions_mod_approved_mcq",name="mod_show_approved_mcq"),
    url(r'^moderator/cq_approved/$',"interface.views.show_questions_mod_approved_cq",name="mod_show_approved_cq"),
    url(r'^moderator/(?P<id>\d+)/$',"interface.views.approve_questions",name="mod_questions"),
    url(r'^moderator/(?P<id>\d+)/approve/$',"interface.views.approve_questions_accept",name="mod_approve"),
    url(r'^moderator/(?P<id>\d+)/postcomment/$',"interface.views.post_comment",name="mod_approve_posted"),
                      
    url(r'^reviews/$',"interface.views.show_reviews",name="show_review"),
    url(r'^ratings/$',"interface.views.show_ratings",name="show_ratings"),


  
]
