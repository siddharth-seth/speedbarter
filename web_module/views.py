from django.contrib.auth.forms import AuthenticationForm
from django.core.context_processors import csrf
from django.shortcuts import render

# Create your views here.


def home(request):
    """
    Serves the home page
    """
    context = {}
    context.update(csrf(request))
    if not request.user.is_authenticated():
        context['login_form'] = AuthenticationForm()
    return render(request, "index.html", context)