from django.db import models

class AttrsMixin:
    def attrs(self):
        for attr, value in self.__dict__.iteritems():
            if not attr.startswith('_'):
                yield attr, value

class MeetupGroup(models.Model, AttrsMixin):
    group_id = models.CharField(max_length=20)
    link = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    photo_url = models.CharField(max_length=200)
    description = models.TextField()
    members = models.CharField(max_length=10)

class MeetupEvent(models.Model, AttrsMixin):
    group = models.ForeignKey(MeetupGroup)
    event_id = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    rsvpcount = models.CharField(max_length=10)
    rsvpable = models.CharField(max_length=20)
    time = models.DateTimeField()
    description = models.TextField()
    venue_name = models.CharField(max_length=50)
    venue_address = models.CharField(max_length=200)
    event_url = models.CharField(max_length=200)

class MeetupEventComment(models.Model, AttrsMixin):
    group = models.ForeignKey(MeetupGroup)
    event = models.ForeignKey(MeetupEvent)
    event_comment_id = models.CharField(max_length=20)
    member_name = models.CharField(max_length=50)
    member_id = models.CharField(max_length=20)
    comment = models.TextField()

