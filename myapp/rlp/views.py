from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from rlp.models import movie
from codecha import Codecha

def post_method(request):
    codecha_challenge = request.POST.get('codecha_challenge_field', False)
    codecha_response  = request.POST.get('codecha_response_field', False)

    recaptcha_challenge = request.POST.get('recaptcha_challenge_field', False)
    recaptcha_response  = request.POST.get('recaptcha_response_field', False)

    codecha_key   = "388abddd7c81403c9f0b7f8f934684e9"
    recaptcha_key = "RECAPTCHA PRIVATE KEY"

    ip = __get_ip(request)
    
    if codecha_challenge and codecha_response:
        codecha_success = Codecha.verify(codecha_challenge, codecha_response, ip, codecha_key)
    elif recaptcha_challenge and recaptcha_response:
        codecha_success = Codecha.verify(recaptcha_challenge, recaptcha_response, ip, recaptcha_key)
    else:
        codecha_success = False

    if codecha_success:
        #success response
        return True
    else:
        #failure response
        return False

def __get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None and post_method(request):
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
            state = "Your username and/or password were incorrect or failed to complete the code."

    return render_to_response('rlp.html',{'state':state, 'username': username},context_instance=RequestContext(request))
