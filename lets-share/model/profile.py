from google.appengine.ext import db
import logging
from corporate import Corporate
from properties import utils

class Profile(db.Model):
	name = db.StringProperty()
	gender = db.StringProperty(choices=['male','female'])
	phone = db.StringProperty()
	email = db.EmailProperty()
	address = db.TextProperty()
	corporate = db.ReferenceProperty(Corporate, collection_name="profiles")
	city = db.StringProperty()
	pincode = db.StringProperty()
	user_id = db.StringProperty()

	

class ProfileDetail():
	def get_fields(self):
		return Profile.properties().keys()
		

	def get_profile(self, user_id):
		q = Profile.gql("WHERE user_id = '"+user_id+"'")
		selectedProfile = None
		for p in q.run(limit = 1):
			selectedProfile = p

		return selectedProfile

	def get_profiles_for_corporate(self, corporate): 	
		return Profile.all().filter('corporate = ', corporate).fetch(limit = 100)


	def save_profile(self, profileContent, profile = Profile()):
		if profile is None:
			profile = Profile()

		for name, property_type in Profile.properties().items():
			logging.info("Setting Field : " + name)
			value = utils.cast(profileContent[name], property_type)			

			setattr(profile, name, value)

		profile.put()
