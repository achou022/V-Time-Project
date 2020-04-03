import csv
import random
import os
from apps.event_app.models import Job, Event, Post, Comment
from .models import User
import bcrypt
from datetime import date, datetime

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = [
    os.path.join(THIS_FOLDER, 'first_names.csv'),
    os.path.join(THIS_FOLDER, 'last_names.csv'),
    os.path.join(THIS_FOLDER, 'companies.csv')]
f = open(my_file[0])
l = open(my_file[1])
c = open(my_file[2])
csv_f = csv.reader(f)
csv_l = csv.reader(l)
csv_c = csv.reader(c)
first_names = []
last_names = []
companies_dict = []
users = []
events = []
companies = []
categories = []
job_types = []
for row in csv_f:
    first_names.append(row[2])
for row in csv_l:
    last_names.append(row[0])
for row in csv_c:
    companies_dict.append(row[1])
event_dict = [
    'walk',
    'run',
    'picknick',
    'soup kitchen',
    'awareness thing',
    'bowling night',
    'pizza party',
    'code-a-thon'
]
category_dict = [
    'Monopoly',
    'Wildlife Conservation Organizations',
    'Pet and Animal Welfare Organizations',
    'Hunting & Fishing Conservation Groups',
    'Zoos and Aquariums',
    'Environmental Conservation & Protection',
    'Parks and Nature Centers',
    'International Development NGOs',
    'Disaster Relief & Humanitarian NGOs',
    'Peace & Human Rights NGOs',
    'Conservation NGOs',
    'Child Sponsorship Organizations',
    'Disease & Disorder Charities',
    'Medical Services & Treatment',
    'Medical Research Charities',
    'Patient and Family Support Charities',
    'Private Elementary, Jr. High, and High Schools',
    'Universities and Colleges',
    'Scholarship and financial aid services',
    'School Reform and Experimental Education',
    'Support for students, teachers, and parents',
]
job_type_dict = [
    'General Services',
    'Program Manager',
    'Program Supervisor',
    'Program Coordinator',
    'Executive Assistant',
    'Community Relations Manager',
    'Development Director',
    'Sponsorship Coordinator',
    'Communications Assistant',
    'Development Specialist',
    'Community Market Manager',
    'Fund Development Coordinator',
    'Donor Relations',
    'Volunteer Coordinator',
    'Volunteer Services Specialist',
    'Event Coordinator',
    'Campaign Coordinator',
    'Catering Sales Manager',
    'Cleaning Crew',
    'Host',
    'Convention and Catering Operations Manager',
    'Catering Services Manager',
    'Bartender',
    'Banquet Servers',
    'Catering Manager',
    'Restaurant and Catering Operations Manager',
    'Catering and Convention Services Manager',
    'Social Catering Manager',
    'Assistant Catering Director',
    'Director of Special Events',
    'Catering and Specials Events Manager',
    'Event Manager',
    'Site Development and Programming',
    'Director of Event Services',
    'Sponsorship Coordinator',
]

website_dict=[
    'https://www.codingdojo.com/',
    'https://www.apple.com/',
    'https://www.microsoft.com/en-us/',
    'https://www.w3schools.com/',
    'https://getbootstrap.com/',
    'https://www.washington.edu/',
    'https://smile.amazon.com/',
    'https://www.lipsum.com/',
    'https://picsum.photos/',
    'https://plot.ly/python/',
    'https://wwf.panda.org/'
]
def generate_names(num=50):
    for i in range(num):
        f_name_index = random.randint(0, len(first_names)-1)
        l_name_index = random.randint(0, len(last_names)-1)
        users.append([first_names[f_name_index],last_names[l_name_index].title()])
    return users
def generate_companies(num=10):
    for i in range(num):
        company_index = random.randint(0, len(companies_dict)-1)
        companies.append(companies_dict[company_index])
    return companies
def generate_events(num=10):
    for i in range(num):
        event_index = random.randint(0, len(event_dict)-1)
        l_name_index = random.randint(0, len(last_names)-1)
        events.append(f"{last_names[l_name_index]}'s {event_dict[event_index]}")
    return events
def generate_categories(num=len(category_dict)):
    for i in range(num):
        category_index = random.randint(0, len(category_dict)-1)
        categories.append(category_dict[category_index])
    return categories
def generate_jobTypes(num=len(job_type_dict)):
    for i in range(num):
        job_types.append([job_type_dict[i], f"The job {job_type_dict[i]} is hard to do"])
    return job_types
def assign_jobs():
    for user in User.objects.all():
        jobs_holder=[]
        event_holder=[]
        for job in user.jobs.all():
            jobs_holder.append(job)
        for job in jobs_holder:
            event_holder.append(job.event)    
        for i in range (random.randint(1,15)):
            new_job = Job.objects.get(id=random.randint(1, len(Job.objects.all())-1))
            job_check = False
            if len(new_job.user.all()) < new_job.required_amount:
                job_check = True
            if new_job not in jobs_holder and new_job.event not in event_holder and job_check: #dont apply over the required amount
                jobs_holder.append(new_job) #doing this so the jobs added are unique and random
                event_holder.append(new_job.event)
        for job in jobs_holder:
            user.jobs.add(job)
def make_default_users():
    fizz_flag=False
    steve_flag=False
    for user in User.objects.all():
        if user.alias=='best boi':
            fizz_flag=True
        if user.alias=='MacMaster':
            steve_flag=True
    if not fizz_flag:
        User.objects.create(first_name='fizz',last_name='ness', alias="best boi", level=9 ,email=f'fizz@gmail.com',pw=bcrypt.hashpw('fizz'.encode(), bcrypt.gensalt()).decode(), birthday=datetime.today(), phone_number='(949)123-4565')
    if not steve_flag:
        User.objects.create(first_name='Steve',last_name='Jobs', alias="MacMaster", level=9 ,email=f'hello123@apple.com',pw=bcrypt.hashpw('hello123'.encode(), bcrypt.gensalt()).decode(), birthday=datetime.today(), phone_number='(949)123-4565')

s_nouns = ["A dude", "My mom", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman"]
p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats", "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen"]
s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on", "retards", "meows on", "flees from", "tries to automate", "explodes"]
p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "retard", "meow on", "flee from", "try to automate", "explode"]
infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.", "for a disease.", "to be able to make toast explode.", "to know more about archeology."]
def make_sentence():
    random_words = [random.choice(s_nouns), random.choice(s_verbs), random.choice(s_nouns).lower() or random.choice(p_nouns).lower(), random.choice(infinitives)]
    new_sentence = " "
    new_sentence = new_sentence.join(random_words)
    return new_sentence
def make_posts():
    for event in Event.objects.all():
        if(len(event.posts.all())<3):
            for i in range(random.randint(1,3)):
                Post.objects.create(user=User.objects.get(id=random.randint(1,len(User.objects.all()))), event=event, message=make_sentence())
def make_comments():
    for post in Post.objects.all():
        if(len(post.comments.all())<3):
            for i in range(random.randint(2,5)):
                Comment.objects.create(user=User.objects.get(id=random.randint(1,len(User.objects.all()))), post=post, comment=make_sentence())

def add_website():
    for company in Company.objects.all():
        company.website=website_dict[random.randint(0, len(website_dict)-1)]
        company.save()