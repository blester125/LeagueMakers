import webapp2

from controllers.MainPage import *
from controllers.AboutHandler import *
from controllers.ManageHandler import *
from controllers.ResultsHandler import *
from controllers.RankHandler import *
from controllers.Admin import *
from controllers.Leagues import *
from controllers.Members import *
from controllers.EmailService import *
from controllers.UploadHandler import *
from controllers.HistoryHandler import *
from controllers.TournamentHandler import *

from controllers.MatchupHandler import *	

app = webapp2.WSGIApplication([
	('/', MainPage),
  ('/results', ResultsHandler),
  ('/ranking', RankHandler),
  ('/manage', ManageHandler),
  ('/about', AboutHandler),
  ('/history', HistoryHandler),
  ('/tournament', TournamentHandler),
  ('/reportTournament', ReportTournament),
  ('/showTournament', ShowTournamentHandler),
  ('/makeLeague', CreateLeague),
  ('/switchLeagues', SwitchLeague),
  ('/match_create', MatchupHandler),
  ('/resetScores', ResetScores),
  ('/deleteLeague', DeleteLeague),
  ('/addAdmin', AddAdmin),
  ('/deleteAdmin', DeleteAdmin),
  ('/deleteMember', DeleteMember),
  ('/addMember', AddMember),
  ('/getUserInfo', getUserInfoHandler),
  ('/showAdmins', showAdminsHandler),
  ('/showLeagues', YourLeagues),
  ('/leagueInfo', LeagueInfo),
  ('/emailservice', EmailService),
  ('/upload', UploadHandler),
	], debug=True)