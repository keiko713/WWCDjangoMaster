from django.db import models

class MeetupGroup(models.Model):
    group_id = models.CharField(max_length=20)
    link = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    photo_url = models.CharField(max_length=200)
    description = models.TextField()
    members = models.CharField(max_length=10)

class MeetupEvent(models.Model):
    group_id = models.ForeignKey(MeetupGroup)
    event_id = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    rsvpcount = models.CharField(max_length=10)
    rsvpable = models.CharField(max_length=20)
    time = models.DateTimeField()
    description = models.TextField()
    venue_name = models.CharField(max_length=50)
    venue_address = models.CharField(max_length=200)
    event_url = models.CharField(max_length=200)

class MeetupEventComment(models.Model):
    group_id = models.ForeignKey(MeetupGroup)
    event_id = models.ForeignKey(MeetupEvent)
    member_name = models.CharField(max_length=50)
    member_id = models.CharField(max_length=20)
    comment = models.TextField()

