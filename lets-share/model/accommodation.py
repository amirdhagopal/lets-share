from google.appengine.ext import db
import logging
from corporate import Corporate
from profile import Profile

class Accommodation(db.Model):
	profile = db.ReferenceProperty(Profile, collection_name="schedules")
	requirement = db.StringProperty()
	accommodationtype = db.StringProperty()
	bedrooms = db.IntegerProperty()
	minbudget = db.IntegerProperty()
	maxbudget = db.IntegerProperty()
	locality=db.StringProperty()
	city=db.StringProperty()


class AccommodationDetail():
	def get_fields(self):
		return ['profile', 'requirement', 'accommodationtype', 'bedrooms', 'minbudget', 'maxbudget', 'locality', 'city']

	def save_accommodation(self, accommodationContent):
		accommodation = Accommodation()
		for field in self.get_fields():
			logging.info("Setting Field : " + field)
			setattr(transport, field, accommodationContent[field])

		transport.put()
