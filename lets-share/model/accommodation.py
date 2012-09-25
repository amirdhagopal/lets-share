from google.appengine.ext import db
import logging
from corporate import Corporate
from profile import Profile, ProfileDetail
from properties import utils

class Accommodation(db.Model):
	profile = db.ReferenceProperty(Profile, collection_name="accommodations")
	requirement = db.StringProperty()
	accommodationtype = db.StringProperty()
	bedrooms = db.IntegerProperty()
	minbudget = db.IntegerProperty()
	maxbudget = db.IntegerProperty()
	locality=db.StringProperty()
	city=db.StringProperty()
	isactive = db.BooleanProperty()


class AccommodationDetail():
	def get_field_names(self):
		return Accommodation.properties().keys()

	def get_accommodation(self, id):
		return Accommodation.get_by_id(id)

	def get_accommodations_for_profile(self, profile):
		return Accommodation.all().filter('profile = ', profile).fetch(limit = 100)

	def get_accommodations_for_corporates(self, corporate):
		profiles = ProfileDetail().get_profiles_for_corporate(corporate)
		return Accommodation.all().filter('profile IN ', profiles).filter('isactive = ', True).fetch(limit = 100)


	def save_accommodation(self, accommodationContent, accommodation):
		if accommodation is None:
			accommodation = Accommodation()

		for name, property_type in Accommodation.properties().items():
			logging.info("Setting Field : " + name)
			value = utils.cast(accommodationContent[name], property_type)

			setattr(accommodation, name, value)

		accommodation.put()
