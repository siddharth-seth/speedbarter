from uuid import uuid4
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model, authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.utils.http import is_safe_url
from speedbarter import settings

__author__ = 'Anant'

User = get_user_model()


def signup_page(request):
    """
    On valid form validation insert user credentials in database
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form_r = RegistrationForm(request.POST)
        if form_r.is_valid():
            # Generates a unique string to be used to activate the account
            activation_key = str(uuid4())

            # Creates and saves the User in the database
            user = User.objects.create_user(
                username=form_r.cleaned_data['username'],
                password=form_r.cleaned_data['password1'],
                email=form_r.cleaned_data['email'],
                active_key=activation_key,
                verified=False
            )

            #Generate and Send the verification email
            request_host = request.get_host()
            subject = "Verify Your Email"
            message = "Hi,\n" \
                      "Thank you for signing up,to activate your account enter the following key: \n" \
                      ""+activation_key+ " \n" \
                      "at "+request_host+"/activate or " \
                      "visit "+request_host+"/activate?activation_key="+activation_key+"\n" \
                      "Thanks, \n" \
                      "Tidor"
            sender = 'info@tidor.com'
            recipients = [form_r.cleaned_data['email']]
            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/')
    else:
        form_r = RegistrationForm()

    context = {
        'form_r': form_r
    }
    return render(request, 'Registration/signup.html', context)


def account_login(request):
    """
    Authenticates and logs in a accounts
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    if request.method == 'POST':
            #Ensure the accounts-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # If accounts account is activated complete log in.
                    login(request, user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    return HttpResponseRedirect('/account/activate')
    else:
        login_form = AuthenticationForm()

    context = {
        'login_form': login_form
    }
    #context.update(csrf(request))
    return render(request, 'index.html', context)


def account_logout(request):
    logout(request)
    return HttpResponseRedirect('/')