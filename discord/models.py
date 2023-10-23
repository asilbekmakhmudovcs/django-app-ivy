from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)        # creator of that group #if user gets deleted, his rooms stay!
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)       # topic name  IF some topics gets deleted it doesnt affect the topic of room

    topic_name = models.CharField(max_length=200) # takes no more than 200 characters
    description = models.TextField(null=True, blank=True)   # null= true means it can be blank, null is False by default
                                                            # blank = we can even submit if we dont write anything AND allows people to add description later
    participants = models.ManyToManyField(User, related_name='participants', blank=True)      # users that have joined the room
    '''Many to many field means each intance of the Model's certain attribute
    can be associated with multiple instances of other model's attibutes'''

    '''example: student vs courses! Student have multiple courses, courses have multiple students'''
    '''One to many (Foreignkey)  student have multiple assignments but assignments cant have multpile student
    for the sake of discussion, believe that example'''

    updated = models.DateField(auto_now=True) # whenever someone changes the something take a time stamp    probably room
    created = models.DateField(auto_now_add=True) # stores a time when someone creates a room.
                                                # difference between [auto_now=True] vs [auto_now_add=True]
                                # auto_now takes time stamp whenever we change. so it takes multiple time stamps
                                # auto_now_add takes only one time stamp



    class Meta:
        ordering = ['updated', '-created']


    def __str__(self):
        return self.topic_name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)   # DateTIME field is for storing the minute as well, unlike DateField that only stores with hours
    created = models.DateTimeField(default=timezone.now)


    class Meta:
        ordering = ['updated', '-created']

    def __str__(self):
        return self.body[:50]
        return self.body[:50]


