from django.shortcuts import render
from .tasks import timemanager


def main(request):
    data = timemanager()
    data
    
    return  render( request, 'main/main_page.html', {'data':data})









