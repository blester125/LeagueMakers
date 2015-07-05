import webapp2

from google.appengine.ext import ndb

class HistoryModel(ndb.Model):
  date = ndb.DateTimeProperty(auto_now_add=True)
  playerA = ndb.StringProperty()
  playerA_rank = ndb.IntegerProperty()
  playerB = ndb.StringProperty()
  playerB_rank = ndb.IntegerProperty()
  winner = ndb.StringProperty()