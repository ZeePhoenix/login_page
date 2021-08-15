from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
	errors = User.objects.basic_validatior(request.POST)
	
	if len(errors) > 0:
		for key, val in errors.items():
			messages.error(request, val)
		return redirect("/")
	else:
		password = request.POST['pass']
		pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
		print(pw_hash)
		user = User.objects.create(
			first_name = request.POST['fname'],
			last_name = request.POST['lname'],
			email_address = request.POST['email'],
			password = pw_hash)
		request.session['userid'] = user.id
		return redirect("/success")

def login(request):
	user = User.objects.filter(email_address=request.POST['email'])
	if user:
		logged_user = user[0]
		if bcrypt.checkpw(request.POST['pass'].encode(), logged_user.password.encode()):
			request.session['userid'] = logged_user.id
			print("Logged into the Mainframe")
			return redirect("/success")
	return redirect('/')

def success(request):
	try:
		user = User.objects.filter(id=request.session['userid'])
	except:
		return redirect("/")
		
	context = { 'user' : user[0] }
	return render(request, "success.html", context)

def logout(request):
	request.session.clear()
	return redirect("/")