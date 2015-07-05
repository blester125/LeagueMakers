import os
import urllib
import webapp2
import logging

from google.appengine.api import mail
from google.appengine.api import *
from views.RenderTemplate import *
from models.MemberModel import *
from models.LeagueModel import *

class EmailService(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()
		if not user:
			render_template(self, 'error_no_user.html', { 'url': users.create_login_url('/manage')})
			return
		template_params = {
			'user': True,
			'user_email': user.email(),
			'rank_active': True,
			'url': users.create_logout_url('/'),
		}
		league_key_string = self.request.get("league_key_string")		
		if not league_key_string:
			render_template(self, 'error_no_league.html', template_params)
			return
		
		league_key = ndb.Key(urlsafe=league_key_string)
		sender_address = user.email()
		subject = self.request.get('subject')
		body = self.request.get('note')
		body = body + "\n\nTo see your ranking, visit our website:\nhttp://leaguemakers.appspot.com/"
		sent_to="<br>"
				
		members = MemberModel.query(ancestor=league_key)
		for member in members:
			if member.email != "":
				mail.send_mail(sender_address, member.email, subject, body)
				sent_to = sent_to + member.email + '<br>'
				
		self.response.out.write('<html><body>Great news!  Your email(s) have been sent!  Click <a href="/manage?league_key_string='+league_key_string+'"> here </a>to return to the league manage page.' + sent_to +'</body></html>')