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
from model.transport import TransportDetail
from model.accommodation import AccommodationDetail
from model.corporate import CorporateDetail

jinja_environment = jinja2.Environment( loader = jinja2.FileSystemLoader(os.path.dirname(__file__) ))
html_path = 'html/'	
template_path = 'template/'
page_path =  html_path + 'page.html'

class CommonUtils():
    def get_template_values(self):
        template_values = {}
        template_values['logout_url'] = users.create_logout_url("/")
        return template_values

class BaseHandler(webapp2.RequestHandler):
    pass
        

class ProfileHandler(BaseHandler):
    def get(self):
    	template_values = CommonUtils().get_template_values()
        user = users.get_current_user()
        corporates = CorporateDetail().get_all_corporates()

        profile = ProfileDetail().get_profile(user.user_id())
        if profile is not None:
            for field in ProfileDetail().get_fields():
                template_values[field] = getattr(profile, field)
        
    	template_values['header'] = user.nickname()
    	template_values['page_title'] = 'Profile Details'
    	template_values['form_name'] = template_path + 'profile_form.template'
        template_values['corporates'] = corporates

    	template = jinja_environment.get_template(page_path)
    	self.response.out.write(template.render(template_values))

    def post(self):
    	fields = ProfileDetail().get_fields()
    	profileContent = {}
    	for field in fields:
    		profileContent[field] = cgi.escape(self.request.get(field))

        corporate_id = int(cgi.escape(self.request.get('corporate')))
        profileContent['corporate'] = CorporateDetail().get_corporate_by_id(corporate_id)

        user = users.get_current_user()

        profile = ProfileDetail().get_profile(user.user_id())

        profileContent['user_id'] = user.user_id()

        logging.info(profileContent)

    	ProfileDetail().save_profile(profileContent, profile)

        self.redirect("/transport")

class TransportHandler(BaseHandler):
    def get(self):
        template_values = CommonUtils().get_template_values()
        
        transport_id_str = self.request.get('id')
        transport_id = (int(transport_id_str) if transport_id_str else 0)
        transport = None
        if(transport_id != 0):
            transport = TransportDetail().get_transport(transport_id)
            template_values['transportid'] = transport_id
        
        if transport is not None:
            for field in TransportDetail().get_fields():
                template_values[field] = getattr(transport, field)
        
        template_values['header'] = users.get_current_user().nickname()
        template_values['page_title'] = 'Transport Details'
        template_values['form_name'] = template_path + 'transport_form.template'
        
        
        template = jinja_environment.get_template(page_path)
        self.response.out.write(template.render(template_values))

    def post(self):
        transportid_str = cgi.escape(self.request.get('transportid'))
        transportid = (int(transportid_str) if transportid_str else 0)
        transport = None
        if(transportid != 0):
            transport = TransportDetail().get_transport(transportid)

        fields = TransportDetail().get_fields()
        transportContent = {}
        for field in fields:
            transportContent[field] = cgi.escape(self.request.get(field))

        user = users.get_current_user()
        transportContent['profile'] = ProfileDetail().get_profile(user.user_id())

        logging.info(transportContent)

        TransportDetail().save_transport(transportContent, transport)

        self.redirect("/accommodation")

class TransportListHandler(BaseHandler):
    def get(self):
        template_values = CommonUtils().get_template_values()
        template_values['header'] = users.get_current_user().nickname()
        template_values['page_title'] = 'Transport List'
        template_values['form_name'] = template_path + 'transport_list.template'
        template_values['transports'] = TransportDetail().get_transports_for_corporates(None)
        template = jinja_environment.get_template(page_path)
        self.response.out.write(template.render(template_values))



class AccommodationHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        accommodation_id_str = self.request.get('id')
        accommodation_id = (int(accommodation_id_str) if accommodation_id_str else 0)
        accommodation = None

        template_values = CommonUtils().get_template_values()
        if(accommodation_id != 0):
            accommodation = AccommodationDetail().get_accommodation(accommodation_id)
            template_values['accommodationid'] = accommodation_id
        
        if accommodation is not None:
            for field in AccommodationDetail().get_fields():
                template_values[field] = getattr(accommodation, field)
        
        
        template_values['header'] = user.nickname()
        template_values['page_title'] = 'Accommodation Details'
        template_values['form_name'] = template_path + 'accommodation_form.template'
        template = jinja_environment.get_template(page_path)
        self.response.out.write(template.render(template_values))

    def post(self):
        accommodationid_str = cgi.escape(self.request.get('accommodationid'))
        accommodationid = (int(accommodationid_str) if accommodationid_str else 0)
        logging.info(accommodationid)
        accommodation = None
        if(accommodationid != 0):
            accommodation = AccommodationDetail().get_accommodation(accommodationid)
        
        logging.info(accommodation)
        fields = AccommodationDetail().get_fields()
        accommodationContent = {}
        for field in fields:
            accommodationContent[field] = cgi.escape(self.request.get(field))

        user = users.get_current_user()
        accommodationContent['profile'] = ProfileDetail().get_profile(user.user_id())

        AccommodationDetail().save_accommodation(accommodationContent, accommodation)

        self.redirect("/services")

class CorporateHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        template_values = CommonUtils().get_template_values()
        template_values['header'] = 'Corporate Details'
        template_values['page_title'] = 'Corporate Details'
        template_values['form_name'] = template_path + 'corporate_form.template'
        template = jinja_environment.get_template(page_path)
        self.response.out.write(template.render(template_values))

    def post(self):
        fields = CorporateDetail().get_fields()
        corporateContent = {}
        for field in fields:
            corporateContent[field] = cgi.escape(self.request.get(field))

        CorporateDetail().save_corporate(corporateContent)

        self.redirect("/services")

class ServicesHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        template_values = CommonUtils().get_template_values()
        template_values['header'] = user.nickname()
        template_values['page_title'] = 'Services'
        template_values['form_name'] = template_path + 'services_list.template'
        template = jinja_environment.get_template(page_path)
        self.response.out.write(template.render(template_values))
