import webapp2

from google.appengine.ext import ndb

class MatchUpModel(ndb.Model):
  round_num = ndb.IntegerProperty()
  playerA = ndb.StringProperty()
  playerB = ndb.StringProperty()