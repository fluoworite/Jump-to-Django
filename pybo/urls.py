from django.urls import path

from .views import QuestionListView, QuestionDetailView, AnswerCreateView
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', QuestionListView.as_view(), name='index'),
    path('<int:pk>/', QuestionDetailView.as_view(), name='detail'),
    path('<int:question_id>/answer/', AnswerCreateView.as_view(), name='answer_create'),
    path('question/create/', views.QuestionCreateView.as_view(), name='question_create'),
]