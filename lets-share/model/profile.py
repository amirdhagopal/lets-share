from google.appengine.ext import db
import logging
from corporate import Corporate

class Profile(db.Model):
	name = db.StringProperty()
	gender = db.StringProperty(choices=['male','female','transgender'])
	phone = db.StringProperty()
	email = db.EmailProperty()
	address = db.StringProperty()
	corporate = db.ReferenceProperty(Corporate, collection_name="profiles")
	city = db.StringProperty()
	pincode = db.StringProperty()
	user_id = db.StringProperty()

	

class ProfileDetail():
	def get_fields(self):
		return ['name', 'gender', 'phone', 'email', 'address', 'corporate', 'city', 'pincode', 'user_id']

	def get_profile(self, user_id):
		q = Profile.gql("WHERE user_id = '"+user_id+"'")
		selectedProfile = None
		for p in q.run(limit = 1):
			selectedProfile = p

		return selectedProfile

	def save_profile(self, profileContent, profile = Profile()):
		if profile is None:
			profile = Profile()

		for field in self.get_fields():
			logging.info("Setting Field : " + field)
			setattr(profile, field, profileContent[field])

		profile.put()
