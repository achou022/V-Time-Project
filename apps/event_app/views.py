from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, Post, Job, Comment, JobType
from ..login_app.models import User
from ..company_app.models import Company


# redners event register menu if user is signed in
def registerMenu(request):
    if 'user' in request.session:
        user=User.objects.get(id=request.session['user'])
        context={
            'companies':user.company_admin.all(),
            'jobs':JobType.objects.all()
        }
        return render(request, 'register_event.html', context)
    else:
        return redirect('/')

# splash page for all existing events in db, does not require user to be signed in
# to view page
def eventSplash(request):
    context={
        'events':Event.objects.all()
    }
    if 'user' in request.session:
        context['user']=User.objects.get(id=request.session['user'])
        context['jobs']=JobType.objects.all()
    return render(request, 'event_splash.html', context)

# event profile page of a specific event identified by the id in the url
# does not require user to be sign in to view
def eventDashboard(request, event_id):
    if 'user' in request.session:
        context={
            'event': Event.objects.get(id=event_id),
            'user':User.objects.get(id=request.session['user'])
        }
    else:
        context={
            'event':Event.objects.get(id=event_id)
        }
    return render(request, 'event_dashboard.html', context)

# registration method for events
# fixes needed: job does not register
def register(request):
    errors=Event.objects.register_validator(request.POST) #need time validation in validator
    if validation(request, errors):
        # insert new position methods
        event=Event.objects.create(name=request.POST['name'], description=request.POST['description'], owner=Company.objects.get(id=request.POST['owner']), address=request.POST['address'], email=request.POST['email'], time=request.POST['time'])

        create_jobs(request, event.id)
        if 'website' in request.POST:
            event.website=request.POST['website']
        if 'contributors' in request.POST:
            event.contributors.add(Company.objects.get(id=request.POST['contributor']))
        if 'sponsors' in request.POST:
            event.sponsors.add(Company.objects.get(id=request.POST['sponsor']))
        return redirect('/event/splash')
    else:
        return redirect('/')

# edit method to edit upcoming event information
# fixes needed: need method for modifying associated jobs
def edit(request, event_id):
    errors=Event.objects.edit_validator(request.POST, event_id)
    if validation(request, errors):
        event=Event.objects.get(id=event_id)
        event.description=request.POST['description']
        event.time=request.POST['time']
        event.address=request.POST['address']
        event.email=request.POST['email']
        # need a way to delete jobs
        create_jobs(request, event_id)
        event.save()
        
        return redirect(f'/event/dashboard/{event_id}')
    else:
        return redirect(f'/event/edit/menu/{event_id}')

def create_jobs(request, event_id):
    print('starting create jobs')
    new_jobs = [[key, val] for key, val in request.POST.items() if 'amount' in key]
    for job in new_jobs:
        Job.objects.create(jobType=JobType.objects.get(id=job[0][7:]), event=Event.objects.get(id=event_id), hours=4, required_amount=job[1])

# renders edit menu for editing event
# mush be signed in to render
def editMenu(request, event_id):
    if 'user' in request.session:
        context={
            'event': Event.objects.get(id=event_id),
            'jobs':JobType.objects.all()
        }
        return render(request, 'edit_event.html', context)
    else:
        return redirect('/')

# menu to join an event
# only render when user is signed in
def jobMenu(request, eventID):
    if 'user' in request.session:
        context={
            'event':Event.objects.get(id=eventID)
        }
        return render(request, 'register_job.html', context)
    else:
        return redirect('/')

# method for user to signup for a job of event
def jobSignUp(request, eventID):
    if 'user' in request.session:
        # errors=Job.objects.expired()
        user=User.objects.get(id=request.session['user'])
        newJob=Job.objects.get(id=request.POST['jobID'])
        for job in user.jobs.all():
            if job.event.id==newJob.event.id:
                return redirect(f'/event/dashboard/{eventID}')
        if newJob.required_amount>len(newJob.user.all()):
            newJob.user.add(user)
        return redirect(f'/event/dashboard/{eventID}')
    else:
        return redirect('/')

def deleteJob(request, eventID, jobID):
    # TO DO- check if user is admin for event
    Job.objects.get(id=jobID).delete()
    return eventDashboard(request, eventID)
    
# method for creating new post to event
def newPost(request, eventID): 
    if 'user' in request.session:
        errors=Post.objects.create_validator(request.POST)
        if validation(request, errors):
            Post.objects.create(user=User.objects.get(id=request.session['user']), event=Event.objects.get(id=eventID),message=request.POST['message'])
        return redirect(f'/event/dashboard/{eventID}')
    else:
        return redirect('/')

# method for creating new comment to post
def newComment(request, postID):
    if 'user' in request.session:
        errors=Comment.objects.create_validator(request.POST)
        if validation(request, errors):
            post=Post.objects.get(id=postID)
            Comment.objects.create(user=User.objects.get(id=request.session['user']),post=post, comment=request.POST['comment'])
        return redirect(f'/event/dashboard/{post.event.id}')
    else:
        return redirect('/')

# helper method: validates and generate error messages
def validation(request, errors):
    if(len(errors)>0):
        for key, val in errors.items():
            messages.error(request, val)
            return False
    return True