import webapp2

from google.appengine.ext import ndb

class MemberModel(ndb.Model):
  name = ndb.StringProperty()
  email = ndb.StringProperty()
  rank = ndb.IntegerProperty(default=1400)
  picture = ndb.StringProperty(default="")