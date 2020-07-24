from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib import messages

from .models import User, Transfer

# Create your views here.
def index(request):
    request.session.flush() # Resets Selected User
    context = {'index_page': 'active'}
    return render(request, "credits/index.html", context)


def all_users(request):
    if request.method == "GET":
        users = User.objects.all()
        context = {'users_page': 'active'}
        context.update({'users': users})
        return render(request, "credits/users.html", context)
    else:
        userID = request.POST['userID']
        user = User.objects.get(pk=userID)
        request.session['username'] = user.name
        request.session['userid'] = user.id 
        return redirect('transfer')

def transfer(request):
    context = {'transfer_page': 'active'}
    if request.session.has_key('userid'):
        other_users = User.objects.exclude(pk=request.session['userid'])
        context.update({'users': other_users})
    if request.method == "POST":
        sender = User.objects.get(pk=request.POST['from-user'])
        receiver = User.objects.get(pk=request.POST['to-user'])
        credits = int(request.POST['credits'])

        if sender.credits < credits:
            messages.warning(request, 'Not Enough Credits to Transfer!')

        else:
            try:
                transfer = Transfer(from_user=sender, to_user=receiver, credits=credits)
                transfer.save()
                
                sender.credits -= credits
                sender.save()
                receiver.credits += credits
                receiver.save()

                messages.success(request, 'Credits Transfered Successfully!')
            except Exception as e:
                print(e)
                messages.warning(request, 'Something Went Wrong!')

    return render(request, "credits/transfer.html", context)