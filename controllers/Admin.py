import webapp2
import json

from google.appengine.api import users
from models.LeagueModel import *
from views.RenderTemplate import *

class AddAdmin(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    league_key_string = self.request.get("league_key_string")
    league_key = ndb.Key(urlsafe=league_key_string)
    league_model = league_key.get()
    if not checkAdmin(league_model, user.email()):
      return
    admin_email = self.request.get("admin_email")
    if admin_email == "":
      return
    league_model.admins.append(admin_email)
    league_model.put()
    return

class DeleteAdmin(webapp2.RequestHandler):
  def get(self):
    league_key_string = self.request.get("league_key_string")
    league_key = ndb.Key(urlsafe=league_key_string)
    league_model = league_key.get()
    if not checkAdmin(league_model, users.get_current_user().email()):
      return
    admins = league_model.admins
    result = []
    tmp = {}
    tmp['name'] = league_model.name
    result += [tmp]
    for i in admins:
      temp = {}
      temp['name'] = i
      result += [temp]      
    self.response.out.write(json.dumps(result))

  def post(self):
    league_key_string = self.request.get("league_key_string")
    league_key = ndb.Key(urlsafe=league_key_string)
    league_model = league_key.get()
    if not checkAdmin(league_model, users.get_current_user().email()):
      return
    admin_email = self.request.get("admin_email")
    if admin_email == "":
      return
    admins = league_model.admins
    if len(admins) == 1:
      render_template(self, '/error_no_admins.html', {
        'user': True,
        'user_email': users.get_current_user().email(),
        'url': users.create_logout_url('/'),
        'league_selected': True,
        'league_key_string': league_key_string
      })
      return
    admins.remove(admin_email)
    league_model.admins = admins
    league_model.put()

class showAdminsHandler(webapp2.RequestHandler):
  def get(self):
    league_key_string = self.request.get("league_key_string")
    league_key = ndb.Key(urlsafe=league_key_string)
    league_model = league_key.get()
    if not checkAdmin(league_model, users.get_current_user().email()):
      return
    admins = league_model.admins
    result = []
    tmp = {}
    tmp['name'] = league_model.name
    result += [tmp]
    for i in admins:
      temp = {}
      temp['name'] = i
      result += [temp]      
    self.response.out.write(json.dumps(result))

def checkAdmin(league_model, email):
  for i in league_model.admins:
    if i == email:
      return True
  return False   
        

