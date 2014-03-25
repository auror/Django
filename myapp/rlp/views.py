from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from rlp.models import movie

def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                state = "You're successfully logged in!"
            elif user.is_active:
                login(request, user)
                state = ''
                
                for i in movie.objects.all():
                    state = state + i.name + ' ' + str(i.year_released) + ' ' + i.actor + ' ' + i.actress + '\n'
                #state = str()
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('rlp.html',{'state':state, 'username': username},context_instance=RequestContext(request))
