import webapp2

from google.appengine.ext import ndb
from models.MatchUpModel import *

class LeagueModel(ndb.Model):
  name = ndb.StringProperty()
  match_ups = ndb.StructuredProperty(MatchUpModel, repeated=True)
  admins = ndb.StringProperty(repeated=True)
  date_created = ndb.DateTimeProperty(auto_now_add=True)
  tournaments = ndb.StringProperty(repeated=True)