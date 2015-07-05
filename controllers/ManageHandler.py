import webapp2
import json

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images

from google.appengine.api import users
from views.RenderTemplate import *
from models.LeagueModel import *
from models.MemberModel import *
from controllers.Admin import checkAdmin

class ManageHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    upload_url = blobstore.create_upload_url('/upload')
    if not user:
      render_template(self, "/error_no_user.html", {'url':user.create_login_url('/manage')})
      return
    league_key_string = self.request.get("league_key_string")
    template_params = {
      'user': True,
      'user_email': user.email(),
      'url': users.create_logout_url('/'),
      'manage_active': True,
      'upload_url': upload_url
    }
    if league_key_string:
      #get the key
      league_key = ndb.Key(urlsafe=league_key_string)
      qry = MemberModel.query(MemberModel.email == user.email(), ancestor=league_key).count()
      if qry != 0:
        template_params['member'] = True
      #get the model
      league_model = league_key.get()
      #True so bottom of sidebar shows up and right half of navbar
      template_params['league_selected'] = True
      #name for the navbar and sidebar
      template_params['league_name'] = league_model.name
      #urlsafestring to pass the league from page to page
      template_params['league_key_string'] = league_key.urlsafe()
      #check for admin
      if checkAdmin(league_model, user.email()):
        template_params['admin'] = True
    #render template
    render_template(self, '/manage.html', template_params)

class getUserInfoHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    members = MemberModel.query(MemberModel.email == user.email())
    result = []
    for i in members:
      rank_num = 1
      temp = {}
      temp['name'] = i.key.parent().get().name
      temp['urlkey'] = i.key.parent().get().key.urlsafe()
      for j in MemberModel.query(ancestor=i.key.parent().get().key).order(-MemberModel.rank):
        if j.email == user.email():
          temp['rank'] = rank_num
          break
        rank_num = rank_num + 1
      temp['score'] = i.rank
      result += [temp]
    self.response.out.write(json.dumps(result))