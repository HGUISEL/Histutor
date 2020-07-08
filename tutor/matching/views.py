from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from .models import Post, Topic, User
from .forms import PostForm, ReportForm, SignupForm

# DEFAULT PAGE
def index(request):
    if request.user.is_authenticated:
        return redirect('tutee_home/')
    else:
        return redirect('/accounts/login/')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('/matching') # redirect으로 tutee home으로 이동
    else:
        form = SignupForm()
    return render(request, 'matching/signup.html', {
        'form' : form,
    })

def tutorReport(request):
    post = Post.objects.last()
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.tutor = User.objects.last()
            report.tutee = User.objects.get(id = post.user.id)
            report.post = Post.objects.get(id = post.id)
            report.save()
    else: 
        form = ReportForm()

    ctx = {
        'post': post,
        'form': form,
    }

    return render(request, 'matching/tutor_report.html', ctx)

def post_new(request):
    ctx={}

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            # return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()


    ctx['form'] = form

    return render(request, 'matching/post_edit.html', ctx)

def tutee_home(request):
    return render(request, 'matching/tutee_home.html', {})