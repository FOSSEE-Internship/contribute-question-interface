from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from interface.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',show_home,name="home"),

    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', logout_page,name="logout_page"),
    url(r'^register/$', register, name="register_page"),
    url(r'^dashboard/$',next_login,name="next_login"),

    url(r'^showquestions/$',show_all_questions,
        name="show_all_questions"),
    url(r'^reallyshowquestions/$',really_show_all_questions,
        name="show_all_questions"),
    url(r'^addquestion/$',add_question,name="add_question"),
    url(r'^addquestion/(?P<question_id>\d+)/$',add_question,
        name="add_question"),
    url(r'^show_review_questions/$', show_review_questions,
        name="show_review_questions"),
    url(r'^checkquestion/(?P<question_id>\d+)/$',
        check_question,name="check_question"),
    url(r'^postreview/(?P<submit>skip|submit)/(?P<question_id>\d+)/$',
        post_review,name="post_review"),
]
