__author__ = 'ggarcia'

import requests

class ngclass:
    def __init__ (self):
        self.base_url="https://www.neighbourly.com/api"
        self.project_id = "5734bf1cb9918e1880f27a6e"

    def get_page(self, url):
        """ Get a page and return a json object asociated"""
        url = "%s%s" %(self.base_url, url)
        print url
        r=requests.get(url)
        if r.status_code == 200:
            return r.json()
        return []

    def get_project_info(self):
        """ Return a json for the info project """
        url="/projects/%s" %(self.project_id,)
        return self.get_page(url)

    def get_all_events(self):
        """ Get all the events information """
        url = "/projectEvents/%s/all" %(self.project_id, )
        return self.get_page(url)

    def get_event_voluteers(self, event_id):
        """ Get the voluteers associated with an event """
        url="/projectEventVolunteers/%s/all/bystatus?projectEventId=%s&targetProjectId=&status=1" %(event_id, event_id)
        return self.get_page(url)

    def get_profile(self, user_id):
        """ """
        url="/profiles/%s" %(user_id, )
        return self.get_page(url)

    def volunteer_in_db(self, volunteer_object):
      volunteer_id=db(db.volunteer.volunteer_id == volunteer_object['id']).select(db.volunteer.id).first()
      if volunteer_id is None:
        return None
      return volunteer_id['id']

    def get_volunteer_id(self, volunteer_object):
      ## check if exists
      if 'id' not in volunteer_object.keys():
        raise "Not an volunteer object"

      volunteer_id=self.volunteer_in_db(volunteer_object)
      if volunteer_id is None:
        location_id=self.get_location_id(volunteer_object['publicLocation'])
        volunteer_id=db.volunteer.insert(volunteer_id=volunteer_object['id'],
                                         first_name=volunteer_object['firstName'],
                                         last_name=volunteer_object['lastName'],
                                         roles=volunteer_object['roles'],
                                         # thumbnail=volunteer_object['thumbnail']['url'],
                                         biography=volunteer_object['biography'],
                                         public_location=location_id)
      return volunteer_id

    def event_in_db(self, event_object):
      event_id=db(db.event.event_id == event_object['id']).select(db.event.id).first()
      if event_id is None:
        return None
      else:
        return event_id['id']

    def get_event_id(self, event_object):
      ## check if exists
      if 'id' not in event_object.keys():
        raise "Not an event object"

      event_id=self.event_in_db(event_object)
      if event_id is None:
        print "Event not present, inserting"
        organiser_id = self.get_volunteer_id(self.get_profile(event_object['organiserId'])) ## TODO: This makes unnecesary requests to the page
        location_id = self.get_location_id(event_object['location'])
        event_id=db.event.insert(event_id=event_object['id'],
                                 name=event_object['name'],
                                 status=event_object['status'],
                                 end_date_time=event_object['endDateTime'],
                                 organiser_id=organiser_id,
                                 location_id=location_id)
      return event_id

    def location_in_db(self, location_object):
      location_id=db((db.location.latitude == location_object['latitude']) and
                     (db.location.longitude == location_object['longitude']) and
                     (db.location.post_code == location_object['postCode'])).select(db.location.id).first()

      if location_id is None:
        return None
      return location_id['id']

    def get_location_id(self, location_object):
      """  """
      if 'latitude' not in location_object.keys():
        raise "Not a location object"

      location_id=self.location_in_db(location_object)
      if location_id is None:
        location_id=db.location.insert(town=location_object['town'],
                                       city=location_object['city'],
                                       country=location_object['country'],
                                       longitude=location_object['longitude'],
                                       latitude=location_object['latitude'],
                                       street=location_object['street'],
                                       post_code=location_object['postCode'],
                                       post_code_prefix=location_object['postCodePrefix'])
      return location_id

    def put_voluteer_in_event(self, event_id, volunteer_id):
      """ insert a volunteer in an event """

      ig = db((db.event_volunteer.event_id == event_id) and (db.event_volunteer.volunteer_id == volunteer_id)).select().first()
      if ig is None:
        ig = db.event_volunteer.insert(event_id=event_id, volunteer_id=volunteer_id)
      return ig

    def check_events(self):

      ## get all events
      events = self.get_all_events()
      for event in events[:10]:
        event_id = self.get_event_id(event)
        print "%s, %s" %(event_id, event['name'])
        for volunteer in self.get_event_voluteers(event['id']):
          vol_id = self.get_volunteer_id(self.get_profile(volunteer['userId']))
          self.put_voluteer_in_event(event_id, vol_id)

      return None

def api_test():
  nbg = ngclass()
  events = nbg.check_events()


  # for event in events[:1]:
  #   print event['name'], event['id'], event['status'], event['endDateTime']
  #   print nbg.get_event_id(event)
  #
  # for user in nbg.get_event_voluteers("585ea7adc7ac880cdcf3817b"):
  #   print user



  return dict()