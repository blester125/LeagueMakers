import webapp2

from google.appengine.api import users
from views.RenderTemplate import *
from models.MemberModel import *
from models.LeagueModel import *
from google.appengine.ext import blobstore
from controllers.Admin import checkAdmin
from google.appengine.api import images

class RankHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      render_template(self, 'error_no_user.html', { 'url': users.create_login_url('/manage')})
      return
    league_key_string = self.request.get("league_key_string")
    template_params = {
      'user': True,
      'user_email': user.email(),
      'rank_active': True,
      'url': users.create_logout_url('/'),
    }
    if not league_key_string:
      render_template(self, 'error_no_league.html', template_params)
      return
    league_key = ndb.Key(urlsafe=league_key_string)
    league_model = league_key.get()
    if checkAdmin(league_model, user.email()):
      template_params['admin'] = True
    members = MemberModel.query(ancestor=league_key).order(-MemberModel.rank)
    number_of_members = MemberModel.query(ancestor=league_key).count()
	
    template_params['zipped_ordered_list'] = zip(range(1,number_of_members+1), members)
    template_params['league_selected'] = True
    template_params['league_name'] = league_model.name
    template_params['league_key_string'] = league_key.urlsafe()
	
    render_template(self, '/ranking.html', template_params)