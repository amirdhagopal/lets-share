from google.appengine.ext import db
import logging
from corporate import Corporate
from profile import Profile, ProfileDetail

class Accommodation(db.Model):
	profile = db.ReferenceProperty(Profile, collection_name="accommodations")
	requirement = db.StringProperty()
	accommodationtype = db.StringProperty()
	bedrooms = db.StringProperty() #TODO: Integer
	minbudget = db.StringProperty() #TODO: Integer
	maxbudget = db.StringProperty() #TODO: Integer
	locality=db.StringProperty()
	city=db.StringProperty()


class AccommodationDetail():
	def get_fields(self):
		return ['profile', 'requirement', 'accommodationtype', 'bedrooms', 'minbudget', 'maxbudget', 'locality', 'city']

	def get_accommodation(self, id):
		return Accommodation.get_by_id(id)

	def get_accommodations_for_profile(self, profile):
		return Accommodation.all().filter('profile = ', profile).fetch(limit = 100)

	def get_accommodations_for_corporates(self, corporate):
		profiles = ProfileDetail().get_profiles_for_corporate(corporate)
		return Accommodation.all().filter('profile IN ', profiles).fetch(limit = 100)


	def save_accommodation(self, accommodationContent, accommodation):
		if accommodation is None:
			accommodation = Accommodation()

		for field in self.get_fields():
			logging.info("Setting Field : " + field)
			setattr(accommodation, field, accommodationContent[field])

		accommodation.put()
