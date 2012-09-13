from google.appengine.ext import db

class Profile(db.Model):
	name = db.StringProperty()
	gender = db.CategoryProperty()
	phone = db.PhoneNumberProperty()
	email = db.EmailProperty()
	address1 = db.StringProperty()
	address2 = db.StringProperty()
	city = db.StringProperty()
	pincode = db.IntegerProperty()

	

class ProfileDetail():
	def get_fields(self):
		return ['name', 'gender'] #, 'phone', 'email', 'address1', 'address2', 'city', 'pincode']

	def save_profile(self, profileContent):
		profile = Profile()
		for field in self.get_fields():
			setattr(profile, field, profileContent[field])
		# profile.name = profileContent.name
		# profile.gender = profileContent.gender
		# profile.phone = profileContent.phone
		# profile.email = profileContent.email
		# profile.address1 = profileContent.address1
		# profile.address2 = profileContent.address2
		# profile.city = profileContent.city
		# profile.pincode = profileContent.pincode

		profile.put()
