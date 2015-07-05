import webapp2

from google.appengine.api import users
from views.RenderTemplate import *
from models.LeagueModel import *
from controllers.Admin import checkAdmin

class AboutHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      template_params = {
        'user': False,
        'url': users.create_login_url('/manage'),
        'about_active': True
        #no user means no league selected is possible
      }
      render_template(self, 'about.html', template_params)
    else:
      league_key_string = self.request.get("league_key_string")
      template_params = {
        'user': True,
        'user_email': user.email(),
        'url': users.create_logout_url('/'),
        'about_active': True,
      }
      if(league_key_string):
        league_key = ndb.Key(urlsafe=league_key_string)
        league_model = league_key.get()
        if checkAdmin(league_model, users.get_current_user().email()):
          template_params['admin'] = True
        template_params['league_selected'] = True
        template_params['league_name'] = league_model.name
        template_params['league_key_string'] = league_key.urlsafe()
      render_template(self, 'about.html', template_params)