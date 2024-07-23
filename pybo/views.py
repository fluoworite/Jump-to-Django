from urllib import request

import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator

from . import form
from .form import AnswerForm, QuestionForm
from .models import Question, Answer

class QuestionListView(ListView):
    model = Question
    template_name = 'pybo/question_list.html'
    context_object_name = 'question_list'
    ordering = ['-create_date']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = context.get('page_obj')
        return context

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'pybo/question_detail.html'
    context_object_name = 'question'

class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'pybo/question_detail.html'

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        answer = form.save(commit=False)
        answer.question = question
        answer.create_date = timezone.now()
        answer.save()
        return redirect('pybo:detail', pk=question.id)

    def form_invalid(self, form):
        context = {'question': get_object_or_404(Question, pk=self.kwargs.get('question_id')), 'form': form}
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Only POST is possible.')

class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'pybo/question_create.html'
    success_url = reverse_lazy('pybo:index')

    def form_valid(self, form):
        question = form.save(commit=False)
        question.create_date = timezone.now()
        question.save()
        return super().form_valid(form)

def index(request):
    return QuestionListView.as_view()(request)