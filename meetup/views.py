from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from datetime import datetime
from meetup.models import *
from meetup.meetupapi import Meetup


def index(request):
    meetup = Meetup()
    meetup.update_wwc()
    group_list = []

    meetup_groups = MeetupGroup.objects.all()
    for group in meetup_groups:
        meetup_events = MeetupEvent.objects.filter(group=group)
        event_list = []
        for event in meetup_events:
            meetup_comments = MeetupEventComment.objects.filter(event=event, group=group)
            event_list.append({
                'event': event,
                'comments': meetup_comments,
            })
        group_list.append({
            'group': group,
            'event_list': event_list,
        })

    return render_to_response('meetup/index.html', {
        'group_list': group_list,
    }, context_instance=RequestContext(request))

