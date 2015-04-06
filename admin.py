# -*- coding: utf-8 -*-

__author__="aquilax"
__date__ ="$Sep 21, 2010 6:37:58 PM$"

import os

from data import *

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    q = Item.all().order('-created')
    data = {
      'include': '',
      'title': "Администрация",
      'items': q.fetch(30),
      'content': "templates/a_index.html",
    }
    path = os.path.join(os.path.dirname(__file__), 'a_main.html')
    self.response.out.write(template.render(path, data))

class CategoryPage(webapp.RequestHandler):
  def get(self):
    q = MainCategory.all().order('name');
    data = {
      'main': q.fetch(100),
      'include': '',
      'title': "Администрация",
      'content': "templates/a_category.html",
    }
    path = os.path.join(os.path.dirname(__file__), 'a_main.html')
    self.response.out.write(template.render(path, data))

  def post(self):
    save_category(self.request);
    self.redirect('/admin/category');

class PostPage(webapp.RequestHandler):
  def get(self):
    q = SubCategory.all().order('main');
    data = {
      'sc': q.fetch(100),
      'include': '',
      'title': "Администрация",
      'content': "templates/a_post.html",
    }
    path = os.path.join(os.path.dirname(__file__), 'a_main.html')
    self.response.out.write(template.render(path, data))

  def post(self):
    save_post(self.request);
    self.redirect('/admin/post');

class UpdatePage(webapp.RequestHandler):
  def get(self, id):
    q = SubCategory.all().order('main');
    post = get_post(int(id));
    data = {
      'sc': q.fetch(100),
      'include': '',
      'item': post,
      'title': "Администрация",
      'content': "templates/a_postupdate.html",
    }
    path = os.path.join(os.path.dirname(__file__), 'a_main.html')
    self.response.out.write(template.render(path, data))

  def post(self, id):
    update_post(int(id), self.request);
    self.redirect('/admin');

application = webapp.WSGIApplication([('/admin/?', MainPage),
                                      ('/admin/category', CategoryPage),
                                      ('/admin/post', PostPage),
                                      ('/admin/update/(\d+)', UpdatePage),
                                      ], debug=False)

def real_main():
    run_wsgi_app(application)

def profile_main():
    # This is the main function for profiling
    # We've renamed our original main() above to real_main()
    import cProfile, pstats
    prof = cProfile.Profile()
    prof = prof.runctx("real_main()", globals(), locals())
    print "<pre>"
    stats = pstats.Stats(prof)
    stats.sort_stats("time")  # Or cumulative
    stats.print_stats(80)  # 80 = how many to print
    # The rest is optional.
    # stats.print_callees()
    # stats.print_callers()
    print "</pre>"

def real_main():
    run_wsgi_app(application)

main = real_main

if __name__ == "__main__":
    main()