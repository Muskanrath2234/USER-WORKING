from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def user_profile(request):
    profile = request.user.profile
    return render(request, 'user_profile.html', {'profile': profile})
