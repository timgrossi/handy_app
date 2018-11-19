from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['fn']) < 2:
            errors['fn'] = "First name should be at least 2 characters"
        elif postData['fn'].isalpha() is False:
            errors['fn'] = "First name is letters only"
        if len(postData['ln']) < 2:
            errors['ln'] = "Last name should be at least 2 characters"
        elif postData['ln'].isalpha() is False:
            errors['ln'] = "Last name is letters only"
        if not EMAIL_REGEX.match(postData['em']):
            errors['em'] = "Invalid email"
        if len(User.objects.filter(email = postData['em'])) > 0:
            errors['em'] = "Email is already being used"
        if postData['pword'] != postData['confirm']:
            errors['pword'] = "Your passwords dont match!"
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['logem'])) < 1:
            errors['logem'] = "Incorrect email"
        else:
            if not bcrypt.checkpw(postData['logpass'].encode(), User.objects.get(email=postData['logem']).password.encode()):
                errors['logpass'] = "Incorrect password"
        return errors 

class JobManager(models.Manager):   
    def job_validator(self, postData):
        errors = {}
        if len(postData['ti']) < 3:
            errors['ti'] = "Title should be at least 3 characters"
        if len(postData['de']) < 3:
            errors['de'] = "Description should be at least 3 characters"
        if len(postData['loc']) < 3:
            errors['loc'] = "Location should be at least 3 characters"
        return errors

    def update_validator(self, postData):
        errors = {}
        if len(postData['edittitle']) < 3:
            errors['edittitle'] = "Title should be at least 3 characters"
        if len(postData['editdesc']) < 3:
            errors['editdesc'] = "Description should be at least 3 characters"
        if len(postData['editloc']) < 3:
            errors['editloc'] = "Location should be at least 3 characters"
        return errors  

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Job(models.Model):
    title = models.CharField(max_length=45)
    desc = models.TextField()
    location = models.CharField(max_length=45)
    categories = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="userjobs")
    objects = JobManager()