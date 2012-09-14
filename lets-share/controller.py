#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import webapp2
import os
import cgi
import logging
from google.appengine.api import users

from model.profile import ProfileDetail

jinja_environment = jinja2.Environment( loader = jinja2.FileSystemLoader(os.path.dirname(__file__) ))
html_path = 'html/'	
template_path = 'template/'
page_path =  html_path + 'profile_home.html'

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
    	user = users.get_current_user()
    	utils = CommonUtils()
        template_values = utils.get_template_values()
    	template_values['header'] = user.nickname()
    	template_values['page_title'] = 'Profile Details'
    	template_values['form_name'] = template_path + 'profile_form.template'
    	template = jinja_environment.get_template(page_path)
    	self.response.out.write(template.render(template_values))

class ProfileSaveHandler(webapp2.RequestHandler):
    def post(self):
    	fields = ProfileDetail().get_fields()
    	profileContent = {}
    	for field in fields:
    		profileContent[field] = cgi.escape(self.request.get(field))


        user = users.get_current_user()
        profileContent['user_id'] = user.user_id()

        logging.info(profileContent)

    	ProfileDetail().save_profile(profileContent)


    	user = users.get_current_user()
    	utils = CommonUtils()
        template_values = utils.get_template_values()
    	template_values['header'] = user.nickname()
        template_values['page_title'] = 'Transport Details'
    	template_values['form_name'] = template_path + 'transport_form.template'
    	template = jinja_environment.get_template(page_path)
    	self.response.out.write(template.render(template_values))

        
class TransportHandler(webapp2.RequestHandler):
	def get(self):
		pass

class AccommodationHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        utils = CommonUtils()
        template_values = utils.get_template_values()
        template_values['header'] = user.nickname()
        template_values['page_title'] = 'Accommodation Details'
        template_values['form_name'] = template_path + 'accommodation_form.template'
        template = jinja_environment.get_template(page_path)
        self.response.out.write(template.render(template_values))

class ServicesHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        utils = CommonUtils()
        template_values = utils.get_template_values()
        template_values['header'] = user.nickname()
        template_values['page_title'] = 'Services'
        template_values['form_name'] = template_path + 'services_list.template'
        template = jinja_environment.get_template(page_path)
        self.response.out.write(template.render(template_values))



class CommonUtils():
    def get_template_values(self):
        template_values = {}
        template_values['logout_url'] = users.create_logout_url("/")
        return template_values
