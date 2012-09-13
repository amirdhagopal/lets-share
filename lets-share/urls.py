
from controller import ProfileHandler, ProfileSaveHandler

import webapp2

app = webapp2.WSGIApplication([(r'/profile_submit', ProfileSaveHandler),
							   (r'/', ProfileHandler)],
                              debug=True)