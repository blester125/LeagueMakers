import webapp2
import json
import math

from datetime import *
from challonge import * 
from google.appengine.api import users
from models.LeagueModel import *
from models.MemberModel import *
from views.RenderTemplate import *
from controllers.Admin import checkAdmin

## You need to enter your challonge information in three places here to use the challonge features.

class TournamentHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      render_template(self, 'error_no_user.html', { 'url': users.create_login_url()})
      return
    # To use this you need a challonge account and to enter the Username and API
    api.set_credentials(CHALLONG_USERNAME, CHALLONGE_API)
    bracket_url = self.request.get('bracket_url')
    league_key_string = self.request.get('league_key_string')
    if not league_key_string:
      render_template(self, 'error_no_league.html', template_params)
      return
    template_params = {
      'user': True,
      'user_email': user.email(),
      'url': users.create_logout_url('/'),
      'league_key_string': league_key_string,
    }
    league_model = ndb.Key(urlsafe=league_key_string).get()
    template_params['league_selected'] = True
    template_params['league_name'] = league_model.name
    template_params['bracket_url'] = bracket_url
    if checkAdmin(league_model, user.email()):
      template_params['admin'] = True
    else:
      render_template(self, '/tournament.html', template_params)
      return
    if not bracket_url:
      #create bracekt 
      members = MemberModel.query(ancestor=league_model.key).order(-MemberModel.rank)
      template_params['entrants'] = members
      render_template(self,'/tournament_create.html', template_params)
      return
    tournament = tournaments.show(bracket_url)
    matches_to_report = matches.index(tournament['id'], state="open")
    players = []
    for match in matches_to_report:
      p1 = participants.show(tournament['id'], match['player1-id'])['name']
      p2 = participants.show(tournament['id'], match['player2-id'])['name']
      players.append((str(match['id']).strip(), str(match['player1-id']).strip(), str(p1).strip(), str(match['player2-id']).strip(), str(p2).strip(), str(match['identifier'])))
    template_params['matches'] = players
    render_template(self, '/tournament.html', template_params)  

  def post(self):
    # Insert your own CHALLONGE Information.
    api.set_credentials(CHALLONGE_USERANME, CHALLONGE_API)
    league_key_string = self.request.get("league_key_string")
    tournament_type = self.request.get("type") 
    entrants = self.request.get('entrants', allow_multiple=True)
    if len(entrants) < 2:
      self.redirect('/tournament?league_key_string='+league_key_string)
      return
    league_key = ndb.Key(urlsafe=league_key_string)
    league_model = league_key.get()
    if not checkAdmin(league_model, users.get_current_user().email()):
      return
    bracket_name = league_model.name + " " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bracket_url = league_model.name + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    bracket_url = bracket_url.replace(" ","")
    if tournament_type == "swiss":
      rounds = math.floor((len(entrants) * 2) / 3)
      tournaments.create(bracket_name, bracket_url, tournament_type, swiss_rounds=rounds)
    else:
      tournaments.create(bracket_name, bracket_url, tournament_type)
    tournament = tournaments.show(bracket_url)
    for entrant in entrants:
      participants.create(tournament['id'], entrant)
    tournaments.publish(tournament['id'])
    tournaments.start(tournament['id'])
    league_model.tournaments.append(bracket_url)
    league_model.put()
    self.redirect('/tournament?league_key_string='+league_key_string+'&bracket_url='+bracket_url)

class ReportTournament(webapp2.RequestHandler):
  def post(self):
    ## Enter your own challonge information.
    api.set_credentials(CHALLONGE_USERANME, CHALLONGE_API_KEY)
    bracket_url = self.request.get('bracket_url')
    match_id = self.request.get('match_id')
    winner_id = self.request.get('winner_id')
    scores = "1-0"
    tournament = tournaments.show(bracket_url)
    match = matches.show(tournament['id'], match_id)
    if winner_id == str(match['player2-id']):
      scores = "0-1"
    matches.update(tournament['id'], match['id'], scores_csv=scores, winner_id=winner_id)
    results = []
    matches_to_report = matches.index(tournament['id'], state="open")
    for match in matches_to_report:
      temp = {
        'match_id': match['id'],
        'player1_id': match['player1-id'],
        'player1': participants.show(tournament['id'], match['player1-id'])['name'],
        'player2_id': match['player2-id'],
        'player2': participants.show(tournament['id'], match['player2-id'])['name'],
        'identifier': match['identifier'],
      }
      results += [temp]
    self.response.out.write(json.dumps(results))

#rewrite JSON
class ShowTournamentHandler(webapp2.RequestHandler):
  def post(self):
    league_key_string = self.request.get("league_key_string")
    league_key = ndb.Key(urlsafe=league_key_string)
    league_model = league_key.get()
    results = []
    first = {
      'name': league_model.name,
      'key': league_key_string,
    }
    if checkAdmin(league_key.get(), users.get_current_user().email()):
      first['admin'] = True
    results += [first]
    tournaments = league_model.tournaments
    for tournament in reversed(tournaments):
      temp = {
        'name': league_model.name,
        'url': tournament,
        'key': league_key_string,
      }
      results += [temp]
    self.response.out.write(json.dumps(results))