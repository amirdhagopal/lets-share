from google.appengine.ext import db
import logging
from corporate import Corporate

class Profile(db.Model):
	name = db.StringProperty()
	gender = db.StringProperty( choices=['male','female','transgender'])
	phone = db.StringProperty()
	email = db.EmailProperty()
	address = db.StringProperty()
	company = db.ReferenceProperty(Corporate, collection_name="profiles")
	city = db.StringProperty()
	pincode = db.StringProperty()
	user_id = db.StringProperty()

	

class ProfileDetail():
	def get_fields(self):
		return ['name', 'gender', 'phone', 'email', 'company', 'address', 'city', 'pincode', 'user_id']

	def save_profile(self, profileContent):
		profile = Profile()
		for field in self.get_fields():
			logging.info("Setting Field : " + field)
			setattr(profile, field, profileContent[field])

		profile.put()
