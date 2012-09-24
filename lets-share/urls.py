
from controller import *

import webapp2

app = webapp2.WSGIApplication([(r'/profile_submit', ProfileHandler),
							   
							   (r'/transport', TransportHandler),
							   (r'/transport_submit', TransportHandler),
							   (r'/transport_list', TransportListHandler),
							   
							   (r'/accommodation', AccommodationHandler),
							   (r'/accommodation_submit', AccommodationHandler),
							   (r'/accommodation_list', AccommodationListHandler),
							   
							   (r'/corporate', CorporateHandler),
							   (r'/corporate_submit', CorporateHandler),

							   (r'/services', ServicesHandler),
							   
							   (r'/', ProfileHandler)],
                              debug=True)