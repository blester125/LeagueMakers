import webapp2
import json

from google.appengine.api import users
from controllers.Admin import checkAdmin
from models.LeagueModel import *
from models.MemberModel import *
from models.HistoryModel import *

class SwitchLeague(webapp2.RequestHandler):
  def post(self):
    picked = self.request.get("league_pick")
    self.redirect('/manage?league_key_string='+picked) 

class ResetScores(webapp2.RequestHandler):
  def post(self):
    league_key_string = self.request.get("league_key_string")
    league_key = ndb.Key(urlsafe=league_key_string)
    if not checkAdmin(league_key.get(), users.get_current_user().email()):
      return
    members = MemberModel.query(ancestor=league_key)
    for i in members:
      i.rank = 1400
      i.put()
    history = HistoryModel.query(ancestor=league_key)
    for i in history:
      i.key.delete()
    self.redirect('/manage?league_key_string='+league_key_string)  

class DeleteLeague(webapp2.RequestHandler):
  def post(self):
    league_key_string = self.request.get("league_key_string")
    league_key = ndb.Key(urlsafe=league_key_string)
    if not checkAdmin(league_key.get(), users.get_current_user().email()):
      return
    members = MemberModel.query(ancestor=league_key)
    for i in members:
      i.key.delete()
    history = HistoryModel.query(ancestor=league_key)
    for i in history:
      i.key.delete()
    league_key.delete()
    self.redirect('/manage')

class CreateLeague(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    league_name = self.request.get("LeagueName")
    if league_name == "":
      return
    league = LeagueModel()
    league.name = league_name
    league.admins = [user.email()]
    league.tournaments = []
    league_key = league.put()
    self.redirect('/manage?league_key_string='+league_key.urlsafe())

#Json Returned
#  { 'leagues_member': {'name': name, 'key': key}, {},
#    'league_admin': {'name': name, 'key': key}
#  }
class YourLeagues(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user();
    result = {}
    result['league_member'] = []
    result['league_admin'] = []
    members = MemberModel.query(MemberModel.email == user.email())
    for member in members:
      temp = {}
      temp['name'] = member.key.parent().get().name
      temp['key'] = member.key.parent().get().key.urlsafe()
      result['league_member'].append(temp)
    leagues = LeagueModel.query(LeagueModel.admins == user.email())
    for league in leagues:
      temp = {}
      temp['key'] = league.key.urlsafe()
      temp['name'] = league.name
      result['league_admin'].append(temp)
    self.response.out.write(json.dumps(result))

#rewrite JSON to be
# { 'League Info': {'name': name, 'member_num': number},
#   'Members': {'name': name, 'rank': rank},
#              {'name': name, 'rank': rank},
# }
class LeagueInfo(webapp2.RequestHandler):
  def post(self):
    league_key_string = self.request.get('league_key_string')
    league_key = ndb.Key(urlsafe=league_key_string)
    result = []
    league = league_key.get()
    num_members = MemberModel.query(ancestor=league_key).count()
    members = MemberModel.query(ancestor=league_key)
    generalInfo = {}
    if checkAdmin(league_key.get(), users.get_current_user().email()):
      generalInfo['admin'] = True
    else:
      generalInfo['admin'] = False
    generalInfo['league_name'] = league.name
    generalInfo['number'] = num_members
    generalInfo['date'] = league.date_created.strftime('%Y-%m-%d')
    generalInfo['name'] = "null"
    result += [generalInfo]
    for member in members:
      temp = {}
      temp['league_name'] = league.name
      temp['number'] = num_members
      temp['name'] = member.name
      temp['email'] = member.email
      result += [temp]
    self.response.out.write(json.dumps(result))