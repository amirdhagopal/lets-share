from google.appengine.ext import db
import logging
from properties import calculated_property

class Corporate(db.Model):
	name = db.StringProperty()
	city = db.StringProperty()
	description = calculated_property.CalculatedProperty(lambda rec: rec.name + ' - ' + rec.city)

class CorporateDetail():
	def get_fields(self):
		return ['name', 'city']

	def get_all_corporates(self):
		return Corporate().all()

	def get_cities(self):
		return ['Chennai', 'Bangalore', 'Pune', 'Gurgaon']

	def get_corporate_by_id(self, id):
		return Corporate.get_by_id(id)

	def save_corporate(self, corporateContent):
		corporate = Corporate()
		for field in self.get_fields():
			logging.info("Setting Field : " + field)
			setattr(corporate, field, corporateContent[field])

		corporate.put()
