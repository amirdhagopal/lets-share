from google.appengine.ext import db
import logging

class Corporate(db.Model):
	name = db.StringProperty()
	city = db.StringProperty()
	

class CorporateDetail():
	def get_fields(self):
		return ['name', 'gender', 'phone', 'email', 'company', 'address', 'city', 'pincode']

	def save_profile(self, profileContent):
		profile = Profile()
		for field in self.get_fields():
			logging.info("Setting Field : " + field)
			setattr(profile, field, profileContent[field])

		profile.put()
