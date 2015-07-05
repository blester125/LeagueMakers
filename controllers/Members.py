import webapp2
import json

from google.appengine.api import users
from models.MemberModel import *
from controllers.Admin import checkAdmin

class DeleteMember(webapp2.RequestHandler):
  def get(self):
    league_key_string = self.request.get("league_key_string")
    league_key = ndb.Key(urlsafe=league_key_string)
    if not checkAdmin(league_key.get(), users.get_current_user().email()):
      return
    members = MemberModel.query(ancestor=league_key)
    result = []
    for member in members:
      temp = {}
      temp['name'] = member.name
      temp['key'] = member.key.urlsafe()
      result += [temp]
    self.response.out.write(json.dumps(result))
 
  def post(self):
    league_key_string = self.request.get('league_key_string')
    league_key = ndb.Key(urlsafe=league_key_string)
    if not checkAdmin(league_key.get(), users.get_current_user().email()):
      return
    picked = self.request.get('toDelete')
    if picked == "":
      return
    member_key = ndb.Key(urlsafe=picked)
    member_key.delete()
    self.redirect('/manage?mode=leagueInfo&league_key_string='+league_key_string)

class AddMember(webapp2.RequestHandler):
  def post(self):
    league_key_string = self.request.get('league_key_string')
    league_key = ndb.Key(urlsafe=league_key_string)
    if not checkAdmin(league_key.get(), users.get_current_user().email()):
      return
    member_name = self.request.get('memberName')
    member_email = self.request.get('memberEmail')
    if member_name == "" or member_email == "":
      return
    members = MemberModel.query(ndb.OR(MemberModel.name == member_name, MemberModel.email == member_email), ancestor=league_key).count()
    if members > 0:
      return
    member = MemberModel(parent=league_key)
    member.name = member_name
    member.email = member_email
    member.put()
