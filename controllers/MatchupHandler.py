import webapp2

from google.appengine.api import users
from views.RenderTemplate import *
from models.MemberModel import *
from models.LeagueModel import *
from models.MatchUpModel import *
from controllers.Admin import checkAdmin

class MatchupHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      render_template(self, 'error_no_user.html', { 'url': users.create_login_url('/manage')})
      return
    league_key_string = self.request.get("league_key_string")
    template_params = {
      'user': True,
      'user_email': user.email(),
      'url': users.create_logout_url('/'),
      'match_active': True,
    }
    if not league_key_string:
      render_template(self, 'error_no_league.html', template_params)
      return
    league_key = ndb.Key(urlsafe=league_key_string)
    league_model = league_key.get()
    if checkAdmin(league_model, user.email()):
      template_params['admin'] = True
    #if league_model.match_ups is None:
    members=MemberModel.query(ancestor=league_key)
    member_list = []
    matched_up= [] 
    for i in league_model.match_ups:
      playerA_name = i.playerA
      playerB_name = i.playerB
      matched_up.append(playerA_name)
      matched_up.append(playerB_name)
    for i in members:
      if not i.name in matched_up:
        player_name = i.name
        member_list.append(player_name)  
    template_params['member_list'] = member_list
    template_params['league_selected'] = True
    template_params['league_name'] = league_model.name
    template_params['league_key_string'] = league_key.urlsafe()
    render_template(self, '/match_create.html', template_params) 

  def post(self):
    league_key_string = self.request.get("league_key_string") 
    league_key = ndb.Key(urlsafe=league_key_string)
    league_model = league_key.get()
    MUs = league_model.match_ups  
    if not checkAdmin(league_model, users.get_current_user().email()):
      return
    playerA_name = self.request.get('player_one')
    playerB_name = self.request.get('player_two')
    '''failsafe for bad entries'''
    if self.request.get('player_two') =="":
      return
    if self.request.get('player_one') =="":
      return
    number=0
    for i in league_model.match_ups:
      number=number+1
    MU = MatchUpModel()
    MU.round_num = number
    MU.playerA = playerA_name
    MU.playerB = playerB_name
    MUs.append(MU)
    league_model.match_ups = MUs
    league_model.put()
    self.redirect("/match_create?league_key_string="+league_key_string)