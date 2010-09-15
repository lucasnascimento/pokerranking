#!/usr/bin/env python
import cgi
import os
import datetime

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

_DEBUG = True
	
class Ranking(db.Model):
	date = db.DateTimeProperty(auto_now_add=True)
	name = db.StringProperty()
	position = db.IntegerProperty()

class BaseRequestHandler(webapp.RequestHandler):
	def generate(self, template_name, template_values={}):
		values = {}
		values.update(template_values)

		path = os.path.join(os.path.dirname(__file__), template_name)
		self.response.out.write(template.render(path, values, debug=_DEBUG))
		
class MainHandler(BaseRequestHandler):
    def get(self):
        self.generate('ranking.html')
		
class NewRanking(BaseRequestHandler):
	def post(self):
		ranking = Ranking()
		ranking.position = int(self.request.get('position'))
		ranking.date = datetime.datetime.strptime(self.request.get('data'), '%d/%m/%Y')
		ranking.name = self.request.get('name')
		ranking.put()
		self.generate('ranking.html')
	def get(self):
		rankings_query = Ranking.all().order('-name')
		rankings = rankings_query.fetch(100)
		template_values = {
			'rankings': rankings
			}
		self.generate('ranking.html', template_values)
		

application = webapp.WSGIApplication([('/', MainHandler)
							,('/ranking', NewRanking)]
							,debug=True)
def main():
	run_wsgi_app(application)

if __name__ == '__main__':
    main()
