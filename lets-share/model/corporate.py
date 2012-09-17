from google.appengine.ext import db
import logging
from properties import CalculatedProperty

class Corporate(db.Model):
	name = db.StringProperty()
	city = db.StringProperty()
	#description = CalculatedProperty(lambda rec: rec.name + ' - ' + rec.city)

	

class CorporateDetail():
	def get_fields(self):
		return ['name', 'city', 'description']

	def save_profile(self, profileContent):
		profile = Profile()
		for field in self.get_fields():
			logging.info("Setting Field : " + field)
			setattr(profile, field, profileContent[field])

		profile.put()
