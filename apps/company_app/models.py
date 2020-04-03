from django.db import models
import re
from datetime import date, datetime
from apps.login_app.models import User

#-----------------------Managers-------------------------#
class CompanyManager(models.Manager):
    errors={}
    def register_validator(self, postData):
        if len(postData['name'])<2:
            self.errors['name']="must have more than 2 characters in first name"
        #add more validators: name unique, desc>200, address valid usps, website regex valid
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            self.errors['email']='enter valid email'
        if len(postData['description'])<150:
            self.errors['description']='Description should be over 150 characters long'
        return self.errors
    def edit_validator(self, postData, my_id):
        if len(postData['name'])<2:
            self.errors['name']="edit: must have more than 2 characters in name"
        #add more to editing
        return self.errors
#-----------------------Models-------------------------#
class CompanyType(models.Model):
    def __repr__(self):
        return f"< Item from companyType table: {self.category}>"
    category = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #foreign key 'companies'

class Company(models.Model):
    def __repr__(self):
        return f"< Item from company table: {self.name}>"
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=150)
    category = models.ForeignKey(CompanyType, related_name='companies', on_delete=models.CASCADE, default=None, null=True)
    admins = models.ManyToManyField(User, related_name="company_admin")
    address = models.CharField(max_length=45)
    website = models.CharField(max_length=90, default='')
    # color-theme
    email = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CompanyManager()
    #foreign key 'events_owned'
    #foreign key 'events_contributed'
    #foreign key 'events_sponsored'

