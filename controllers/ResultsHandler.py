import webapp2

from google.appengine.api import users
from views.RenderTemplate import *
from models.MemberModel import *
from models.LeagueModel import *
from models.MatchUpModel import *
from models.HistoryModel import *
from controllers.Elo import *
from controllers.Admin import checkAdmin

class ResultsHandler(webapp2.RequestHandler):
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
      'results_active': True,
    }
    if not league_key_string:
      render_template(self, 'error_no_league.html', template_params)
      return
    league_key = ndb.Key(urlsafe=league_key_string)
    league_model = league_key.get()
    if checkAdmin(league_model, user.email()):
      template_params['admin'] = True
    template_params['league_selected'] = True
    template_params['league_name'] = league_model.name
    template_params['league_key_string'] = league_key.urlsafe()
    MUs = []
    for i in league_model.match_ups:
      playerA_name = i.playerA
      playerB_name = i.playerB
      number = i.round_num
      MUs.append((number, playerA_name, playerB_name))
    template_params['match_ups'] = MUs
    render_template(self, '/results.html', template_params) 

  def post(self):
    league_key_string = self.request.get("league_key_string") 
    league_key = ndb.Key(urlsafe=league_key_string)
    league_model = league_key.get()
    if not checkAdmin(league_model, users.get_current_user().email()):
      return
    rounds_reported = self.request.get("rounds_entered").split("-")
    rounds_reported = rounds_reported[:len(rounds_reported)-1]
    MUs = league_model.match_ups  
    for i in rounds_reported:
      history_model = HistoryModel(parent=league_key)
      winner = self.request.get("round"+i+"winner")
      loser = self.request.get("round"+i+"loser")
      members = MemberModel.query(ancestor=league_key)
      for j in members:
        if j.name == winner:
          winner_model = j
          history_model.playerA = j.name
          history_model.playerA_rank = j.rank
          history_model.winner = j.name
        if j.name == loser:
          loser_model = j
          history_model.playerB = j.name
          history_model.playerB_rank = j.rank
      report_and_rank(winner_model, loser_model)
      winner_model.put()
      loser_model.put()
      history_model.put()
      for i in range(0, len(MUs)):
        if MUs[i].playerA == winner or MUs[i].playerB == winner:
          MUs.pop(i)
          break 
    league_model.match_ups = MUs
    league_model.put()
    self.redirect('/results?league_key_string='+league_key_string)