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
from google.appengine.api import users, memcache

from model.profile import ProfileDetail
from model.transport import TransportDetail
from model.accommodation import AccommodationDetail
from model.corporate import CorporateDetail


jinja_environment = jinja2.Environment( loader = jinja2.FileSystemLoader(os.path.dirname(__file__) ))
html_path = 'html/'	
template_path = 'template/'
page_path =  html_path + 'page.html'

class BaseHandler(webapp2.RequestHandler):
    def get_current_profile(self):
        user = users.get_current_user()
        key = 'userid:%s' % user.user_id()
        profile = memcache.get(key)
        if profile is None:
            logging.info('Profile Cache miss.')
            profile = ProfileDetail().get_profile(user.user_id())
            memcache.add(key, profile)
        
        return profile
         

    def get_template_values(self):
        template_values = {}
        template_values['logout_url'] = users.create_logout_url("/")
        template_values['header'] = users.get_current_user().nickname()
        return template_values
        
class HomeHandler(BaseHandler):
    def get(self):
        profile = self.get_current_profile()
        if profile is not None:
            self.redirect("/services")
        else:
            self.redirect("/profile")

class ProfileHandler(BaseHandler):
    def get(self):
    	template_values = self.get_template_values()
        profile = self.get_current_profile()
        template_values['email'] = users.get_current_user().email()
        template_values['name'] = users.get_current_user().nickname().split("@")[0]
        template_values['gender'] = 'female'
        template_values['cities'] = CorporateDetail().get_cities()
        if profile is not None:
            template_values['mode'] = 'editprofile'
            for field in ProfileDetail().get_fields():
                template_values[field] = getattr(profile, field)
        
    	
    	template_values['page_title'] = 'Profile Details'
    	template_values['form_name'] = template_path + 'profile_form.template'
        template_values['corporates'] = CorporateDetail().get_all_corporates()

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

        profile = self.get_current_profile()

        profileContent['user_id'] = user.user_id()

        logging.info(profileContent)

    	ProfileDetail().save_profile(profileContent, profile)

        self.redirect("/transport")

class TransportHandler(BaseHandler):
    def get(self):
        profile = self.get_current_profile()
        transportlist = TransportDetail().get_transports_for_profile(profile)
        if not transportlist:
            self.redirect("/transport_form")
        else:
            self.redirect("/transport_list?profile")


class TransportFormHandler(BaseHandler):
    def get(self):
        template_values = self.get_template_values()
        template_values['cities'] = CorporateDetail().get_cities()
        template_values['city'] = self.get_current_profile().city
        template_values['vehicletype'] = 'four-wheeler'
        template_values['availableseats'] = 2
        template_values['genderpreference'] = ['male','female']
        template_values['departuretime'] = "08:30"

        template_values['isactive'] = True
        transport_id_str = self.request.get('id')
        transport_id = (int(transport_id_str) if transport_id_str else -1)
        transport = None
        if(transport_id != -1):
            transport = TransportDetail().get_transport(transport_id)
            template_values['transportid'] = transport_id
        
        if transport is not None:
            for field in TransportDetail().get_field_names():
                template_values[field] = getattr(transport, field)
        
        template_values['next'] = 'accommodation'
        template_values['page_title'] = 'Transport Details'
        template_values['form_name'] = template_path + 'transport_form.template'
        
        
        template = jinja_environment.get_template(page_path)
        self.response.out.write(template.render(template_values))

    def post(self):
        transportid_str = cgi.escape(self.request.get('transportid'))
        transportid = (int(transportid_str) if transportid_str else -1)
        transport = None
        if(transportid != -1):
            transport = TransportDetail().get_transport(transportid)

        fields = TransportDetail().get_field_names()
        transportContent = {}
        for field in fields:
            transportContent[field] = cgi.escape(self.request.get(field))

        transportContent['genderpreference'] = self.request.get_all('genderpreference')

        transportContent['profile'] = self.get_current_profile()

        logging.info(transportContent)

        TransportDetail().save_transport(transportContent, transport)

        self.redirect("/accommodation")

class TransportListHandler(BaseHandler):
    def get(self):
        template_values = self.get_template_values()
        profile = self.get_current_profile()
        if 'profile' in self.request.arguments():
            transports = TransportDetail().get_transports_for_profile(profile)
            template_values['continue'] = 'accommodation'
            template_values['nav_bar'] = template_path + 'profile_nav_bar.template'
            template_values['mode'] = 'profile'
        else:
            corporate = None if profile is None else profile.corporate
            transports = TransportDetail().get_transports_for_corporates(corporate)
            template_values['nav_bar'] = template_path + 'search_nav_bar.template'
            template_values['mode'] = 'search'

        template_values['addnew'] = 'transport_form'
        template_values['entity'] = 'Transport'
        template_values['showme'] = 'transport'
        template_values['page_title'] = 'Transport List'
        template_values['form_name'] = template_path + 'transport_list.template'
        template_values['transports'] = transports
        template = jinja_environment.get_template(page_path)
        self.response.out.write(template.render(template_values))

class AccommodationListHandler(BaseHandler):
    def get(self):
        template_values = self.get_template_values()
        profile = self.get_current_profile()
        if 'profile' in self.request.arguments():
            accommodations = AccommodationDetail().get_accommodations_for_profile(profile)
            template_values['continue'] = 'services'
            template_values['nav_bar'] = template_path + 'profile_nav_bar.template'
            template_values['mode'] = 'profile'
        else:
            corporate = None if profile is None else profile.corporate
            accommodations = AccommodationDetail().get_accommodations_for_corporates(corporate)
            template_values['nav_bar'] = template_path + 'search_nav_bar.template'
            template_values['mode'] = 'search'
        
        template_values['addnew'] = 'accommodation_form'
        template_values['showme'] = 'accommodation'
        template_values['entity'] = 'Accommodation'
        template_values['page_title'] = 'Accommodation List'
        template_values['form_name'] = template_path + 'accommodation_list.template'
        template_values['accommodations'] = accommodations
        template = jinja_environment.get_template(page_path)
        self.response.out.write(template.render(template_values))

class AccommodationHandler(BaseHandler):
    def get(self):
        profile = self.get_current_profile()
        accommodationlist = AccommodationDetail().get_accommodations_for_profile(profile)
        if not accommodationlist:
            self.redirect("/accommodation_form")
        else:
            self.redirect("/accommodation_list?profile")

class AccommodationFormHandler(BaseHandler):
    def get(self):
        template_values = self.get_template_values()
        template_values['cities'] = CorporateDetail().get_cities()
        template_values['city'] = self.get_current_profile().city
        template_values['isactive'] = True
        template_values['bedrooms'] = 2
        template_values['requirement'] = 'rent'
        template_values['accommodationtype'] = 'apartment'
        template_values['minbudget'] = 5000
        template_values['maxbudget'] = 30000
        
        accommodation_id_str = self.request.get('id')
        accommodation_id = (int(accommodation_id_str) if accommodation_id_str else 0)
        accommodation = None


        if(accommodation_id != 0):
            accommodation = AccommodationDetail().get_accommodation(accommodation_id)
            template_values['accommodationid'] = accommodation_id
        
        if accommodation is not None:
            for field in AccommodationDetail().get_field_names():
                template_values[field] = getattr(accommodation, field)

        template_values['next'] = 'services'
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
        fields = AccommodationDetail().get_field_names()
        accommodationContent = {}
        for field in fields:
            accommodationContent[field] = cgi.escape(self.request.get(field))

        accommodationContent['profile'] = self.get_current_profile()

        AccommodationDetail().save_accommodation(accommodationContent, accommodation)

        self.redirect("/services")

class CorporateHandler(BaseHandler):
    def get(self):
        
        template_values = self.get_template_values()
        
        template_values['page_title'] = 'Corporate Details'
        template_values['form_name'] = template_path + 'corporate_form.template'
        template_values['cities'] = CorporateDetail().get_cities()
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
        
        template_values = self.get_template_values()
        
        template_values['page_title'] = 'Services'
        template_values['form_name'] = template_path + 'services_list.template'
        template = jinja_environment.get_template(page_path)
        self.response.out.write(template.render(template_values))
