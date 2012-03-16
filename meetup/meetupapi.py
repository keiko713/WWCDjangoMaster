import datetime

from django.conf import settings
from meetup.models import *
from meetup.meetup_read_client import Meetup as MeetupClient

class Meetup:
    def update_wwc(self, *args, **kwargs):
        client = MeetupClient(settings.MEETUP_API_KEY)
        group_id = settings.MEETUP_WWC_GROUP_ID

        response = client.get_groups(group_id=group_id)
        group = response.results[0]
        photo_url = ''
        if group.get('group_photo', ''):
            photo_url = group.get('group_photo').get('photo_link')

        g, created = MeetupGroup.objects.get_or_create(
            group_id = group_id,
            defaults = {
                'link': group.get('link', ''),
                'name': group.get('name', ''),
                'photo_url': photo_url,
                'description': group.get('description', ''),
                'members': group.get('members', ''),
            }
        )

        response = client.get_events(group_id=group_id)
        for event in response.results:
            time = event.get('time', '')
            if time:
                event_datetime = datetime.datetime.fromtimestamp(int(time)/1000)

            venue = event.get('venue', '')
            venue_name, venue_address = '', ''
            if venue:
                venue_name = venue.get('name', '')
                venue_address = self.get_venue_address(venue)

            e, created = MeetupEvent.objects.get_or_create(
                group_id = g,
                event_id = event.get('id', ''),
                defaults = {
                    'name': event.get('name', ''),
                    'rsvpcount': event.get('rsvpcount', ''),
                    'rsvpable': event.get('rsvpable', ''),
                    'time': event_datetime if time else None,
                    'description': event.get('description', ''),
                    'venue_name': venue_name,
                    'venue_address': venue_address,
                    'event_url': event.get('event_url', ''),
                }
            )

    def get_venue_address(self, venue):
        address_1 = venue.get('address_1', '')
        address_2 = venue.get('address_2', '')
        address_3 = venue.get('address_3', '')
        city = venue.get('city', 'N/A')
        state = venue.get('state', 'N/A')
        zip = venue.get('zip', '')

        address = []
        if address_1:
            address.append(address_1)
        if address_2:
            address.append(address_2)
        if address_3:
            address.append(address_3)
        if city and state:
            address.append('%s, %s %s' % (city, state, zip))

        return u'\n'.join(address)
