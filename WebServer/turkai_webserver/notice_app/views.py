from django.shortcuts import render

# Create your views here.


def red_notices(request):
    return render(request,'index.html')