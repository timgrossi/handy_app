from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "handy_app/index.html")

def process_new_user(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            p = request.POST['pword']
            pw = bcrypt.hashpw(p.encode(),bcrypt.gensalt())
            User.objects.create(first_name=request.POST['fn'], last_name=request.POST['ln'],email=request.POST['em'],password=pw.decode())
            request.session['welcome'] = User.objects.last().id
            return redirect("/dashboard")

def process_login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        if request.method =="POST":
            request.session['welcome'] = User.objects.filter(email=request.POST['logem']).first().id   
        return redirect("/dashboard")
    
def process_job(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/create_job")
    else:
        if request.method=="POST":
            user_who_posted = User.objects.get(id=request.session['welcome'])
            Job.objects.create(title=request.POST['ti'], desc=request.POST['de'], location=request.POST['loc'], user=user_who_posted)
        return redirect("/dashboard")

def dashboard(request):
    jobs={
        'username' : User.objects.get(id=request.session['welcome']),
        'allthejobs' : Job.objects.all().order_by("-created_at")
        # 'userjobs' : Job.objects.get()
    }
    return render(request, "handy_app/dashboard.html", jobs)

def create(request):
    context ={
        'user' : User.objects.get(id=request.session['welcome'])
    }
    return render(request, "handy_app/createpage.html", context)

def view_job(request, id):
    current = Job.objects.get(id=id)
    currentuser = User.objects.get(id=request.session['welcome'])
    thejobs={
        'viewjob' : current,
        'user' : currentuser
    }
    return render(request, "handy_app/show.html", thejobs)

def edit_job(request, id):
    j = {
        'jobedit' : Job.objects.get(id=id)
    }
    return render(request, "handy_app/edit.html", j)

def process_edit(request, id):
    errors = Job.objects.update_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/jobs/edit/"+id)
    else:
        if request.method=="POST":
            job_to_update = Job.objects.get(id=id)
            job_to_update.title = request.POST['edittitle']
            job_to_update.desc = request.POST['editdesc']
            job_to_update.location = request.POST['editloc']
            job_to_update.save()
    return redirect("/dashboard")

def delete(request, id):
    jobdelete = Job.objects.get(id=id)
    jobdelete.delete()
    return redirect("/dashboard")

def logout(request):
    request.session.clear()
    return redirect('/')