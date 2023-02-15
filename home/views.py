from django.shortcuts import render, HttpResponse ,redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from home.models import Contact,Profile,Product
from django.contrib import messages
from django.views import View
from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView ,PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
#from .forms import User_form
# Create your views here.
from .forms import UpdateUserForm, UpdateProfileForm
from .forms import AddProductForm

def auction(request):
    return render(request,'bid.html')
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            product_name = form.cleaned_data['product_name']
            product_description = form.cleaned_data['product_description']
            product_price = form.cleaned_data['product_price']
            image=request.FILES.get('image')
            product=Product(name=product_name,description=product_description,price=product_price, image=image)
            product.save()
            # Add product to database
            # ...
            return redirect('/')
    else:
        form = AddProductForm()
    return render(request, 'add_product.html', {'form': form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')

@login_required
def user_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'user_profile.html', {'user_form': user_form, 'profile_form': profile_form})
def index(request):
    if request.user.is_anonymous:
        return redirect("/bidders-login/")
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def services(request):
    return render(request, 'services.html')
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'BidderRegistration.html'
    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, "BidderRegistration.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        desc=request.POST.get('message')
        contact=Contact(name=name,email=email,desc=desc)
        contact.save()
        messages.success(request, 'Message Received..:) You will be contacted shortly!!!')
    return render(request, 'contact.html')

'''def b_regis(request):   
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        uname=request.POST.get('uname')
        passwrd=request.POST.get('pass')
        dob=request.POST.get('dob')
        phone=request.POST.get('phone')
        mail=request.POST.get('mail')
        u_type=request.POST.get('type')
        user=User.objects.create_user(First_name=fname,Last_name=lname,username=uname,Password=passwrd,DOB=dob,Phone=phone,email=mail,u_type=u_type)
        if user.is_authenticated:
            messages.success(request, 'Already Registered!!!')
            login(request,user)
            return redirect('/')  
     
        if user is not None:
            messages.success(request, 'Registration Successfull!!!')
            user.save()
            login(request,user)
            return redirect('/')
        else:
            messages.warning(request, 'Registration UnSuccessfull!!!')
            
              
    
    return render(request, 'BidderRegistration.html')'''
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
def b_login(request):
    if request.method=="POST":
        user = authenticate(username=request.POST.get('uname'), password=request.POST.get('pass'))
        if user is not None and user:
            login(request,user)
            return redirect("/")
        else:
            messages.warning(request, 'User Not Found!!!')
            return render(request, 'Bidderlogin.html')
    return render(request, 'Bidderlogin.html')

def log_out(request):
    logout(request)
    return redirect("/")