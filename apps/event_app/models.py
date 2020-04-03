from django.db import models
import re
from datetime import date, datetime
from apps.login_app.models import User
from apps.company_app.models import Company
#-----------------------Managers-------------------------#
class EventManager(models.Manager):
    errors={}
    def email_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            return True
        return False 
    def register_validator(self, postData):
        if len(postData['name'])<2:
            self.errors['name']="must have more than 2 characters in event name"
        eTime=datetime.strptime[postData['time'], '%Y-%m-%d-%H-%M']
        if eTime <datetime.now():
            self.errors['time']="Event time must be in the future!!!"
        #add more validators: name unique, desc>200, address valid usps, website regex valid
        return self.errors
    def edit_validator(self, postData, event_id):
        if len(postData['name'])<2:
            self.errors['name']="edit: must have more than 2 characters in name"
        #add more to editing
        return self.errors
class JobManager(models.Manager):
    errors={}
    def create_validator(self, postData):
        return self.errors
    # def expired(self):
    #     if self.event.time < datetime.now():
    #         self.errors['expiredEvent']='this event has expired and cannot be signed up'
    #     return self.errors
class PostManager(models.Manager):
    errors={}
    def create_validator(self, postData):
        return self.errors
class CommentManager(models.Manager):
    errors={}
    def create_validator(self, postData):
        return self.errors

#-----------------------Models-------------------------#
class JobType(models.Model):
    def __repr__(self):
        return f"< Item from jobtype table: {self.name}>"
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #foreign key 'job_job_type'
    #foreign key 'requiredJobs_name'

class Event(models.Model):
    def __repr__(self):
        return f"< Item from event table: {self.name}>"
    # event methods============================================================

    # return sorted list with most recent to first
    def postsByTime(self):
        return self.posts.all().order_by('created_at').reverse()

    # event fields=============================================================
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=150)
    owner = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="events_owned")
    contributors = models.ManyToManyField(Company, related_name="events_contributed")
    sponsors = models.ManyToManyField(Company, related_name="events_sponsored")
    time = models.DateTimeField(default=datetime.now)
    address = models.CharField(max_length=45, default='')
    website = models.CharField(max_length=90, default='')
    email = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()
    #foreign key 'job_event'
    #foreign key 'posts'

class Job(models.Model):
    def __repr__(self):
        return f"< Item from job table: {self.name}>"
    jobType=models.ForeignKey(JobType, related_name='jobs', on_delete=models.CASCADE)
    # name=jobType.name
    # description=jobType.description
    user = models.ManyToManyField(User, related_name='jobs')
    hours = models.IntegerField(default=4) #change template default
    required_amount=models.IntegerField(default=10)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="job_event")
    review = models.CharField(max_length=150, default="")
    endorsement = models.CharField(max_length=150, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()

class Post(models.Model):
    def __repr__(self):
        return f"< content from post table: {self.message}>"

    # return sorted comments with most recent to first
    def commentsByTime(self):
        return self.comments.all().order_by('created_at').reverse()

    user = models.ForeignKey(User, related_name="user_post", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='posts', on_delete=models.CASCADE)
    message = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()
    #foreign key 'comments'
    
class Comment(models.Model):
    def __repr__(self):
        return f"< content from comment table: {self.comment}>"
    user = models.ForeignKey(User, related_name="user_comment", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    comment = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()

