#!/usr/bin/env python
import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

_DEBUG = True

class Player(db.Model):
	name = db.StringProperty()
	email = db.StringProperty()
	
class Ranking(db.Model):
	date = db.DateTimeProperty(auto_now_add=True)
	player = db.Reference(Player)
	position = db.IntegerProperty()

class BaseRequestHandler(webapp.RequestHandler):
	def generate(self, template_name, template_values={}):
		values = {}
		values.update(template_values)
		directory = os.path.dirname(__file__)
		path = os.path.join(directory, os.path.join('templates', template_name))
		self.response.out.write(template.render(path, values, debug=_DEBUG))
	
class MainHandler(BaseRequestHandler):
    def get(self):
        self.generate('ranking.html')

		
		
class NewRanking(BaseRequestHandler):
	def post(self):
		ranking = Ranking()
		ranking.position = self.request.get('position')
		ranking.date = self.request.get('data')
		ranking.player.name = self.request.get('name')
		ranking.player.email = self.request.get('email')
		ranking.put()
		self.generate('raking.html')
	def get(self):
		players_query = Player.all().order('-name')
		players = players_query.fetch(100)

		template_values = {
			'players': players
			}
		path = os.path.join(os.path.dirname(__file__), 'template.html')
		self.response.out.write(template.render(path, template_values))
		

application = webapp.WSGIApplication([('/', MainHandler)
							,('/newRanking', NewRanking)]
							,debug=True)
def main():
	run_wsgi_app(application)

    


if __name__ == '__main__':
    main()
