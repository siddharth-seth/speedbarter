from django.shortcuts import render

# Create your views here.


def home(request):
    """
    Serves the home page
    """

    return render(request, "index.html", {})