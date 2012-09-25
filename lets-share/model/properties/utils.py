from google.appengine.ext import db
import datetime

def cast(value, property_instance):
	property_type = type(property_instance)
	return_value = value

	if property_type == db.IntegerProperty:
		return_value = int(value)
	elif property_type == db.BooleanProperty:
		return_value = bool(value)

	return return_value






