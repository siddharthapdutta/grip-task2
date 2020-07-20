from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib import messages

from .models import User, Transfer

# Create your views here.
def index(request):
    request.session.flush()
    context = {'index_page': 'active'}
    return render(request, "credits/index.html", context)


def all_users(request):
    if request.method == "GET":
        users = User.objects.all()
        context = {'users_page': 'active'}
        context.update({'users': users})
        return render(request, "credits/users.html", context)
    elif request.method == "POST":
        userID = request.POST['userID']
        user = User.objects.get(pk=userID)
        request.session['username'] = user.name
        request.session['userid'] = user.id 
        return redirect('transfer')
    else:
        raise Http404("Invalid Request")
    

def transfer(request):
    context = {'transfer_page': 'active'}
    if request.session.has_key('userid'):
        other_users = User.objects.exclude(pk=request.session['userid'])
        context.update({'users': other_users})
    if request.method == "POST":
        from_user = request.POST['from-user']
        to_user = request.POST['to-user']
        credits = int(request.POST['credits'])

        transfer = Transfer(from_user=User.objects.get(pk=from_user), to_user=User.objects.get(pk=to_user), credits=credits)
        transfer.save()
        receiver = User.objects.get(pk=to_user)
        receiver.credits += credits
        receiver.save()
        messages.success(request, 'Credits Transfered Successfully!')
    
    return render(request, "credits/transfer.html", context)