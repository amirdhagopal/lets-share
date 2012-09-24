
from controller import *

import webapp2

app = webapp2.WSGIApplication([(r'/profile', ProfileHandler),

							   (r'/transport', TransportHandler),
							   (r'/transport_form', TransportFormHandler),
							   (r'/transport_list', TransportListHandler),
							   
							   (r'/accommodation', AccommodationHandler),
							   (r'/accommodation_form', AccommodationFormHandler),
							   (r'/accommodation_list', AccommodationListHandler),
							   
							   (r'/corporate', CorporateHandler),

							   (r'/services', ServicesHandler),
							   
							   (r'/', HomeHandler)],
                              debug=True)