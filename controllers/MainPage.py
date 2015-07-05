import webapp2
import logging

from google.appengine.api import users
from views.RenderTemplate import *

class MainPage(webapp2.RequestHandler):
	
  def get(self):  
    user = users.get_current_user()

    if not user:
      template_params = {
        'user': False,
        'url': users.create_login_url('/manage')
      }
      render_template(self, 'index.html', template_params)
    else:
      template_params = {
        'user': True,
        'user_email': user.email(),
        'url': users.create_logout_url('/'),
      }
      render_template(self, 'index.html', template_params)
	 