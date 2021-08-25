from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse


@login_required(login_url="/login/")
def home(request):
    return HttpResponse(f"Hello, {request.user.username}")
