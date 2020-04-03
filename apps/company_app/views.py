from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Company, CompanyType
from ..event_app.models import Event, Job, JobType
from ..login_app.models import User
from datetime import datetime
import bcrypt

# render register company menu if logged in
def registerMenu(request):
    if 'user' in request.session:
        return render(request, 'register_company.html')
    else:
        return redirect('/')

# render company profile page, allowed for public view
def profile(request, companyID):
    context={
        'company':Company.objects.get(id=companyID)
    }
    return render(request, 'company_profile.html', context)

#  validation for admin and adjust the admin status once validated
def newAdmin(request, company_id):
    user=User.objects.filter(email=request.POST['admin'])
    if len(user) ==0:
        messages.error(request, 'this email has no associated user')
        return False
    else:
        admin=user[0]
        company=Company.objects.get(id=company_id)
        company.admins.add(admin)
        company.save()
    return True

# edit company, does not allow name field of Company to be edited
# security features need to be edited****
def editCompany(request, company_id):
    errors=Company.objects.edit_validator(request.POST, company_id)
    if validation(request, errors):
        if request.POST['admin'] != "":
            if not newAdmin(request, company_id):
                return redirect('company:editMenu', company_id=company_id)
        company=Company.objects.get(id=company_id)
        company.name=request.POST['name']
        company.email=request.POST['email']
        company.description=request.POST['description']
        company.address=request.POST['address']
        company.website=request.POST['website']
        company.save()
    return redirect('/')

# register a new company
def newCompany(request):
    errors=Company.objects.register_validator(request.POST)
    if validation(request, errors):
        #debugging adding category
        CompanyType.objects.create(category="test category")
        my_category=CompanyType.objects.last()
        #end debugging category
        admin=request.session['user']
        Company.objects.create(name=request.POST['name'], description=request.POST['description'], address=request.POST['address'], website=request.POST['website'], email=request.POST['email'], category=my_category)
        Company.objects.last().admins.add(User.objects.get(id=admin))
        return redirect(f'/dashboard/{admin}/admin')
    else:
        return redirect('/')

# splash page for company, renders thumbnail images of existing companies in database
def companySplash(request):
    context={
        'companies':Company.objects.all()
    }
    if 'user' in request.session:
        context['user']=User.objects.get(id=request.session['user'])
    return render(request, 'company_splash.html', context)

# edit company menu, must be admin of company to edit
def editCompanyMenu(request, company_id):
    if 'user' in request.session:
        context={
            'company': Company.objects.get(id=company_id)
        }
        return render(request, 'edit_company.html', context)
    else:
        return redirect('/')

# helper method: validator for logging error messages
def validation(request, errors):
    if(len(errors)>0):
        for key, val in errors.items():
            messages.error(request, val)
            return False
    return True