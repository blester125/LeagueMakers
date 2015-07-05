import webapp2
import json

from models.HistoryModel import *
from views.RenderTemplate import *
from controllers.Admin import checkAdmin

class HistoryHandler(webapp2.RequestHandler):
  def post(self):
    league_key_string = self.request.get('league_key_string')
    playerA = self.request.get('playerA')
    playerB = self.request.get('playerB')
    league_key = ndb.Key(urlsafe=league_key_string)
    result = {}
    result['league'] = []
    result['history'] = []
    wins = 0
    losses = 0
    full_history = False
    if playerA == '' and playerB == '':
      full_history = True
      history = HistoryModel.query(ancestor=league_key).order(-HistoryModel.date)
    elif playerB == '':
      history = HistoryModel.query(ndb.OR(HistoryModel.playerA == playerA, HistoryModel.playerB == playerA), ancestor=league_key).order(-HistoryModel.date)
    elif playerA == '':
      history = HistoryModel.query(ndb.OR(HistoryModel.playerA == playerB, HistoryModel.playerB == playerB), ancestor=league_key).order(-HistoryModel.date)
    else:
      history = HistoryModel.query(ndb.OR(ndb.AND(HistoryModel.playerA == playerA, 
                                                  HistoryModel.playerB == playerB),
                                          ndb.AND(HistoryModel.playerA == playerB, 
                                                  HistoryModel.playerB == playerA)), ancestor=league_key).order(-HistoryModel.date)
    for i in history:
      if not full_history:
        if playerA == i.winner:
          wins += 1
        else:
          losses += 1
      temp  = {
        'date': i.date.strftime('%Y-%m-%d'),
        'playerA': i.playerA,
        'playerA_rank': i.playerA_rank,
        'playerB': i.playerB,
        'playerB_rank': i.playerB_rank,
        'winner': i.winner
      }
      result['history'].append(temp)
    league = {'name': league_key.get().name,
              'wins': wins,
              'losses': losses}
    result['league'].append(league)
    self.response.out.write(json.dumps(result))