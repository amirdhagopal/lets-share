from google.appengine.ext import db
import logging
from corporate import Corporate
from profile import Profile

class Transport(db.Model):
	profile = db.ReferenceProperty(Profile, collection_name="schedules")
	origin = db.StringProperty()
	destination = db.StringProperty()
	city = db.StringProperty()
	via = db.StringProperty()
	frequency = db.ListProperty()
	vehicletype=db.StringProperty()
	availableseats=db.IntegerProperty()
	genderpreference = db.StringProperty( choices=['male','female','transgender'])
	isactive = db.BooleanProperty()


class TransportDetail():
	def get_fields(self):
		return ['profile', 'origin', 'destination', 'city', 'via', 'frequency', 'vehicletype', 'availableseats', 'genderpreference', 'isactive']

	def save_transport(self, transportContent):
		transport = Transport()
		for field in self.get_fields():
			logging.info("Setting Field : " + field)
			setattr(transport, field, transportContent[field])

		transport.put()
