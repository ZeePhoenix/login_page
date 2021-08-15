from django.db import models
import re

from django.http import request

class UserManager(models.Manager):
	def basic_validatior(self, postData):
		errors = {}
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if len(postData["fname"]) < 2 or not str.isalpha(postData["fname"]):
			errors['fname'] = ("Invalid First Name")
		if len(postData["lname"]) < 2 or not str.isalpha(postData["lname"]):
			errors['lname'] = ("Invalid Last Name")
		if not EMAIL_REGEX.match(postData["email"]):
			errors['email'] = ("Invalid Email Address")
		if len(User.objects.filter(email_address=postData['email'])) > 0:
			errors['email'] = ("Email alread in use")
		if len(postData['pass']) < 8:
			errors['pass'] = ("Password not long enough")
		if not postData['pass'] == postData['pass_confirm']:
			errors['pass_confirm'] = ("Password does not match")
		return errors


# What defines a User
class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email_address = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()