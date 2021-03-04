from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basicValidator(self, formInfo):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        emailTaken = User.objects.filter(email=formInfo['email'])

        if len(formInfo['fname']) == 0:
            errors['firstNameReq'] = "First Name is required"
        elif len(formInfo['fname']) < 2:
            errors['firstnameLength'] = "First Name needs to be at least 2 characters."
        if len(formInfo['lname']) == 0:
            errors['lastNameReq'] = "Last Name is required"
        elif len(formInfo['lname']) < 2:
            errors['lastnameLength'] = "Last Name needs to be at least 2 characters."
        if len(formInfo['email']) == 0:
            errors['emailReq'] = "Email is required"
        elif not EMAIL_REGEX.match(formInfo['email']):            
            errors['invalidEmail'] = "Invalid email address!"
        elif len(emailTaken) > 0:
            errors['emailSnatchedUp'] = "This email is already being used."
        if len(formInfo['pw']) == 0:
            errors['passwordReq'] = "Password is required"
        elif len(formInfo['pw']) < 8:
            errors['passwordLength'] = "Password must be at least 8 characters."
        if formInfo['pw'] != formInfo['cpw']:
            errors['passwordMatch'] = "Passwords must match!"
        return errors
    def loginValidator(self, formInfo):
        errors = {}
        verifyEmail = User.objects.filter(email=formInfo['email'])

        if len(verifyEmail) == 0:
            errors['noEmailFound'] = "This email is not found. Please register."
        elif not bcrypt.checkpw(formInfo['pw'].encode(), verifyEmail[0].password.encode()):
            errors['wrongPassword'] = "Incorrect password. Please try again."
        return errors
    def wishValidator(self, formInfo):
        errors = {}

        if len(formInfo['wish']) == 0:
            errors['WishReq'] = "Please make your wish"
        elif len(formInfo['wish']) < 3:
            errors['wishLength'] = "Wishes need to be at least 3 characters."
        if len(formInfo['desc']) == 0:
            errors['WishDescReq'] = "A description is required"
        elif len(formInfo['desc']) < 3:
            errors['WishDescLength'] = "Description needs to be at least 3 characters."
        return errors

    def editValidator(self, formInfo):
        errors = {}        

        if len(formInfo['wish']) == 0:
            errors['WishReq'] = "Please make your wish"
        elif len(formInfo['wish']) < 3:
            errors['wishLength'] = "Wishes need to be at least 3 characters."
        if len(formInfo['desc']) == 0:
            errors['WishDescReq'] = "A description is required"
        elif len(formInfo['desc']) < 3:
            errors['WishDescLength'] = "Description needs to be at least 3 characters."
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    wish = models.CharField(max_length=255)
    desc = models.TextField()
    user = models.ForeignKey(User, related_name="wishes", on_delete= models.CASCADE)
    granted = models.BooleanField(default=False)
    liked = models.ManyToManyField(User, related_name="liked_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()