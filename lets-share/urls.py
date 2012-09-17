
from controller import *

import webapp2

app = webapp2.WSGIApplication([(r'/profile_submit', ProfileHandler),
							   
							   (r'/transport', TransportHandler),
							   (r'/transport_submit', TransportHandler),
							   
							   (r'/accommodation', AccommodationHandler),
							   (r'/accommodation_submit', AccommodationHandler),
							   
							   (r'/services', ServicesHandler),
							   
							   (r'/', ProfileHandler)],
                              debug=True)