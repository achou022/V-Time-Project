from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from ..event_app.models import Event, Job, JobType
from ..company_app.models import Company, CompanyType
import bcrypt
from .generator import generate_companies, generate_events, generate_names, generate_categories, generate_jobTypes, assign_jobs, make_default_users, make_posts, make_comments, add_website
import random
from datetime import datetime


def getNavBar(request):
    context={}
    if 'user' in request.session:
        context={
            'username':User.objects.get(id=request.session['user'])
        }
    return render(request, 'navBar.html', context)

# redners template for the landing page
# SHOULD NOT REQUIRE TO BE SIGNED IN!!!
def landingPage(request):
    #```````````````I put this in to make a new company`
    context={}
    if 'user' in request.session:
        context={
            'username':User.objects.get(id=request.session['user'])
        }
    #```````````````end new company`
    return render(request, 'landingPage.html', context)

# renders login menu for user login
# SHOULD NOT REQUIRE TO BE SIGNED IN!!!
def loginMenu(request):
    if 'user' in request.session:
        return redirect('/dashboard')
    else:
        return render(request, 'login.html')

# method for logging in user
# SHOULD NOT REQUIRE TO BE SIGNED IN!!!
def login(request):
    errors=User.objects.login_validator(request.POST)
    if validation(request, errors):
        return redirect('/login/menu')
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0] 
            request.session['user']=logged_user.id
        return redirect('/dashboard')

# render register new user menu template
# SHOULD NOT REQUIRE TO BE SIGNED IN!!!
def registerMenu(request):
    if 'user' in request.session:
        return redirect('/event/splash')
    else:
        return render(request, 'register_user.html')

# method for registering new user
# SHOULD NOT REQUIRE TO BE SIGNED IN!!!
def register(request):
    errors=User.objects.register_validator(request.POST)
    if validation(request, errors):
        return redirect('/register/menu')
    else:
        newUser=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'], alias=request.POST['alias'] ,email=request.POST['email'],pw=bcrypt.hashpw(request.POST['password_initial'].encode(), bcrypt.gensalt()).decode(), birthday=request.POST['birthday'], phone_number=request.POST['phone_number'])
        request.session['user']=newUser.id
        return redirect('/dashboard')

# renders dashboard for user if signed in
def dashboard(request):
    if 'user' in request.session:
        user=User.objects.get(id=request.session['user'])
        context={
            'user':user,
            'graph':user.visualStat(),
            'all_users':User.objects.all()
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

# renders admin's dashboard if authorized as admin for company
def adminDashboard(request, adminID):
    if adminID==request.session['user']:
        context={
            'user':User.objects.get(id=request.session['user'])
        }
        return render(request, 'admin_dashboard.html', context)
    else:
        logout(request)
        messages.error(request, 'You are not an admin!')
        return redirect('/login/menu')

# renders user profile page if signed in
def profile(request, userID):
    if 'user' in request.session:
        context={
            'user':User.objects.get(id=userID)
        }
        return render(request, 'user_profile.html', context)
    else:
        user=User.objects.get(id=userID).first_name
        messages.error(request, f"Please signin to view {user}'s profile!")
        return redirect('/login/menu')

# renders user profile edit menu
def editMenu(request):
    if 'user' in request.session:
        context={
            'user':User.objects.get(id=request.session['user'])
        }
        return render(request, 'edit_user.html', context)
    else:
        return redirect('/')


# method to edit user profile
def edit(request):
    if 'user' in request.session:
        user_id=request.session['user']
        user=User.objects.get(id=user_id)
    errors=User.objects.edit_validator(request.POST, user_id)
    if validation(request, errors):
        return redirect('login:editMenu')
    else:
        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.alias=request.POST['alias']
        user.email=request.POST['email']
        user.phone_number=request.POST['phone_number']
        user.description=request.POST['description']
        if request.POST.getlist('adminlevel'):
            print("hello")
            if request.POST.getlist('adminlevel')[0]=='1':
                user.level=9
        user.save()
        return redirect('/dashboard')

# method to log out the user, clears session
def logout(request):
    request.session.clear()
    return redirect('/')

# helper method: validates and logs error messages
def validation(request, errors):
    if(len(errors)>0):
        for key, val in errors.items():
            messages.error(request, (key,val))
            return True
    return False

# generates dummy data for website
def generate(request):
    users = generate_names()
    events = generate_events()
    companies = generate_companies()
    categories = generate_categories()
    job_types = generate_jobTypes()
    if len(User.objects.all())<10:
        for user in users:
            User.objects.create(first_name=user[0],last_name=user[1], alias="bot" ,email=f'{user[0]}{user[1]}@gmail.com',pw=bcrypt.hashpw(user[0].encode(), bcrypt.gensalt()).decode(), birthday=datetime.today(), phone_number='(949)123-4565')
    if len(CompanyType.objects.all())<10:
        for category in categories:
            CompanyType.objects.create(category=category)
    if len(Company.objects.all())<50:
        for company in companies:
            category = CompanyType.objects.get(id=random.randint(1,len(CompanyType.objects.all())))
            newCompany=Company.objects.create(name=company,description='lorem ipsum says....',category=category,address=f'123 st boardwalk ave. suit 1', email=f'company@gg.com', )
            newCompany.admins.add(User.objects.get(id=random.randint(1,len(User.objects.all()))))
    if len(JobType.objects.all())<10:
        for job in job_types:
            JobType.objects.create(name=job[0], description=job[1])
    if len(Event.objects.all())<50:
        for event in events:
            company=Company.objects.get(id=random.randint(1,len(Company.objects.all())))
            newEvent=Event.objects.create(name=event, description=f'This is an event for!!!{company.description}', owner=company, address=f'123 st {company.name}-boardwalk ave. suit 1', email=f'{company.name}@gg.com')
            for i in range(random.randint(2,5)):
                newEvent.sponsors.add(Company.objects.get(id=random.randint(1,len(Company.objects.all()))))
                newEvent.contributors.add(Company.objects.get(id=random.randint(1,len(Company.objects.all()))))

            for i in range (random.randint(2,10)):
                Job.objects.create(jobType=JobType.objects.get(id=random.randint(1,len(JobType.objects.all()))),required_amount=random.randint(1,10), event=Event.objects.last(), hours=random.randint(1,8))
    make_default_users()
    assign_jobs()
    make_posts()
    make_comments()
    add_website()
    return redirect('/')