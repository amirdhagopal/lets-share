
from controller import *

import webapp2

app = webapp2.WSGIApplication([(r'/profile_submit', ProfileSaveHandler),
							   (r'/accommodation_submit', AccommodationHandler),
							   (r'/services', ServicesHandler),
							   (r'/', ProfileHandler)],
                              debug=True)