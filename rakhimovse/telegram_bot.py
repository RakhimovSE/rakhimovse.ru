from django.http import HttpResponse


token = 'PUT_YOUR_TOKEN_HERE'


def index(request):
    return HttpResponse('Yo')
