import os
import webapp2

from google.appengine.ext.webapp import template

#function to render templates
def render_template(handler, templatename, templatevalues):
  path = os.path.join(os.path.dirname(__file__), '../templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)