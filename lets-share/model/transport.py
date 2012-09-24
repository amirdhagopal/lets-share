from google.appengine.ext import db
import logging
from corporate import Corporate
from profile import Profile, ProfileDetail

class Transport(db.Model):
	profile = db.ReferenceProperty(Profile, collection_name="schedules")
	origin = db.StringProperty()
	destination = db.StringProperty()
	city = db.StringProperty()
	via = db.StringProperty()
	departuretime = db.StringProperty()
	frequency = db.StringProperty()
	vehicletype=db.StringProperty()
	availableseats=db.StringProperty() #TODO: Integer
	genderpreference = db.StringProperty( choices=['male','female','transgender'])
	isactive = db.StringProperty() #TODO: Boolean


class TransportDetail():
	def get_fields(self):
		return ['profile', 'origin', 'destination', 'city', 'via', 'departuretime', 'frequency', 'vehicletype', 'availableseats', 'genderpreference', 'isactive']

	def get_transport(self, id):
		return Transport.get_by_id(id)

	def get_transports_for_profile(self, profile):
		return Transport.all().filter('profile = ', profile).fetch(limit = 100)

	def get_transports_for_corporates(self, corporate):
		profiles = ProfileDetail().get_profiles_for_corporate(corporate)
		return Transport.all().filter('profile IN ', profiles).fetch(limit = 100)

	def save_transport(self, transportContent, transport):
		if transport is None:
			transport = Transport()
		for field in self.get_fields():
			logging.info("Setting Field : " + field)
			setattr(transport, field, transportContent[field])

		transport.put()

