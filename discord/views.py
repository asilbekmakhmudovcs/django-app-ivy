from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from templates import *
from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.




def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home_name')

    if request.method == 'POST':
        username1 = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username1)
        except:
            messages.error(request, "User does not exist!")
        else:

            user = authenticate(request, username=username1, password=password)
            """authenticate() returns nothing if the password and username doesn't match"""
            if user is not None:
                login(request, user)
                return redirect('home_name')
            else:
                messages.error(request, "Username or Password does not exist!")

    context = {'page': page}
    return render(request, 'discord/reg_log.html', context)


def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home_name')
        else:
            messages.error(request, 'Problem occured with signing in. Try again.')
    context = {'page':page, 'form':form}
    return render(request, 'discord/reg_log.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # if there is something it will be assigned to q, if false, it will assign nothing
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                    Q(topic_name__icontains=q) |
                                    Q(description__icontains=q) |
                                    Q(host__username__icontains=q)
                                    )   # icontains -> case insensitive while contains -> snsitive

    count = rooms.count()
    topics = Topic.objects.all()

    recent_act_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')

    context = {'rooms': rooms, 'topics': topics, "count": count, 'recent_act_messages': recent_act_messages}
    #context = {'data': something}
    return render(request, "discord/home_old.html", context)



def room(request, pk):
    room = Room.objects.get(id=pk)     # answer for which room?
    participants = room.participants.all()
    msgs = room.message_set.all() # set_all allows to retrieve all related objects(linked with Foreignkey) of Messege class
    '''we use "_set" to one to many, and dont use for ManyToMany()'''
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('message')
        )
        room.participants.add(request.user)
        return redirect('room_name', pk=room.id)


    context = {'sth': room, 'msgs':msgs, 'participants': participants}      # sth is a key that I can access the dictionary of room from

    return render(request, 'discord/rooom.html', context)



def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    recent_act_messages = user.message_set.all().order_by('-created')
    topics = Topic.objects.all()
    #recent_act_messages = Message.objects.filter(Q(room__host_id=pk)).order_by('-created')
    context = {'user': user, "rooms": rooms, 'recent_act_messages': recent_act_messages, 'topics': topics}
    return render(request, 'discord/profile.html', context)


@login_required(login_url='login_name')
def create_room(request):
    context = {"form": RoomForm}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            rm = form.save(commit=False)
            rm.host = request.user
            rm.save()
            return redirect('home_name')


    return render(request, 'discord/room_form.html', context)

@login_required(login_url='login_name')
def update(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!!")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home_name')

    context = {'form': form}
    return render(request, 'discord/room_form.html', context)

@login_required(login_url='login_name')
def deleteRoom(request, pk):
    '''This function deletes many things: comments, rooms..'''
    room=Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!!")
    
    if request.method == 'POST':    # ==> when we click delete button cuz <form method was POST>
        room.delete()
        return redirect('home_name')
    return render(request, 'discord/deleting.html', {"obj": room})


def logoutUser(request):
    logout(request)
    return redirect('home_name')


@login_required(login_url='login_name')
def deletemessage(request, pk):
    '''This function deletes comments'''
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here!!!")

    if request.method == 'POST':  # ==> when we click delete button cuz <form method was POST>
        message.delete()
        return redirect('home_name')
    return render(request, 'discord/deleting.html', {"obj": message})
