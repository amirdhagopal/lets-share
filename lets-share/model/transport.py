from google.appengine.ext import db
import logging
from corporate import Corporate
from profile import Profile, ProfileDetail
from properties import utils

class Transport(db.Model):
	profile = db.ReferenceProperty(Profile, collection_name="schedules")
	origin = db.StringProperty()
	destination = db.StringProperty()
	city = db.StringProperty()
	via = db.StringProperty()
	departuretime = db.StringProperty()
	vehicletype=db.StringProperty( choices=['two-wheeler','four-wheeler'])
	availableseats=db.IntegerProperty()
	genderpreference = db.ListProperty(str)
	isactive = db.BooleanProperty()


class TransportDetail():
	def get_field_names(self):
		return Transport.properties().keys()

	def get_transport(self, id):
		return Transport.get_by_id(id)

	def get_transports_for_profile(self, profile):
		return Transport.all().filter('profile = ', profile).fetch(limit = 100)

	def get_transports_for_corporates(self, corporate):
		profiles = ProfileDetail().get_profiles_for_corporate(corporate)
		return Transport.all().filter('profile IN ', profiles).filter('isactive = ', True).fetch(limit = 100)

	def save_transport(self, transportContent, transport):
		if transport is None:
			transport = Transport()

		for name, property_type in Transport.properties().items():
			logging.info("Setting Field : " + name)
			value = utils.cast(transportContent[name], property_type)			

			setattr(transport, name, value)

		transport.put()

