from django.urls import path
from . import views

urlpatterns=[
    path('',views.index , name='home'),
    path('resume-parse/',views.resume_parse, name='parse_resume'),
]