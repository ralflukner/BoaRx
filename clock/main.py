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

import datetime
import jinja2
import os
import webapp2
import models

from google.appengine.api import users

template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd()))
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        current_time = datetime.datetime.now()
        user = users.get_current_user()
        login_url=users.create_login_url(self.request.path)
        logout_url=users.create_logout_url(self.request.path)        
        
        userprefs = models.get_userprefs()
        if userprefs: current_time += datetime.timedelta(
            0,0,0,0,0, userprefs.tz_offset)
       
        template = template_env.get_template('home.html')
        context = {
            'current_time': current_time,
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'userprefs': userprefs
 		}                   
        self.response.out.write(template.render(context))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
