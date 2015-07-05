import cgi
import logging
import models
import os
import webapp2

from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from models.MemberModel import *

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    user = users.get_current_user()
    league_key_string = self.request.get("league_key_string")
    league_key = ndb.Key(urlsafe=league_key_string)
    upload = self.get_uploads('image')
    blob_key = upload[0].key()
    imgsrc = images.get_serving_url(blob_key, size=32, crop=False, secure_url = None)
    if imgsrc == "":
      return
    logging.warning(imgsrc)
    qry = MemberModel.query(MemberModel.email == user.email(), ancestor=league_key)
    for member in qry:
      member.picture = imgsrc
      member.put()
    self.redirect('/manage?league_key_string=' + league_key_string)