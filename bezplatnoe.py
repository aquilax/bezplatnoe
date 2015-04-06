# -*- encoding: utf-8 -*-

__author__="aquilax"
__date__ ="$Sep 21, 2010 6:37:58 PM$"

import os
import datetime

from data import *
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    hash = 'MainPage';
    page = memcache.get(hash)
    if (not page):
      q = Item.all().order('-created')
      #sc = SubCategory.all().order('name')
      data = {
        'title': "Безплатно е!",
        'maincat' : get_all_main(),
        'content': "templates/index.html",
        'items': q.fetch(10),
      }
      path = os.path.join(os.path.dirname(__file__), 'main.html')
      page = template.render(path, data)
      memcache.add(key=hash, value=page , time=3600);
    self.response.out.write(page)

class CategoryPage(webapp.RequestHandler):
  def get(self, id, slug):
    main = get_main(int(id));
    q = Item.all().filter('main =', main).order('-score').order('-created')
    sc = SubCategory.all().filter('main =', main).order('name')
    data = {
      'mainid': int(id),
      'subid': 0,
      'title': main.name.encode('utf-8') + " &raquo; Безплатно е!",
      'heading': main.name,
      'subcat' : sc.fetch(100),
      'maincat' : get_all_main(),
      'content': "templates/index.html",
      'items': q.fetch(30),
    }
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, data))

class SubCategoryPage(webapp.RequestHandler):
  def get(self, id, slug, slug2):
    sub = get_sub(int(id));
    q = Item.all().filter('sub =', sub).order('-score').order('-created')
    sc = SubCategory.all().filter('main =', sub.main).order('name')
    data = {
      'mainid': sub.main.key().id(),
      'subid': int(id),
      'title': sub.name.encode('utf-8') + ' &raquo; '+sub.main.name.encode('utf-8') + " &raquo; Безплатно е!",
      'heading': sub.main.name.encode('utf-8') + ' &raquo; '+sub.name.encode('utf-8'),
      'subcat' : sc.fetch(100),
      'maincat' : get_all_main(),
      'content': "templates/index.html",
      'items': q.fetch(50),
    }
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, data))

class PostPage(webapp.RequestHandler):
  def get(self, id, slug):
    hash = 'post'+id;
    page = memcache.get(hash)
    if (not page):
      post = get_post(int(id));
      sc = SubCategory.all().filter('main =', post.main).order('name')
      data = {
        'mainid': post.main.key().id(),
        'subid': post.sub.key().id(),
        'title': post.title.encode('utf-8') + " &raquo; Безплатно е!",
        'subcat' : sc.fetch(100),
        'maincat' : get_all_main(),
        'content': "templates/post.html",
        'item': post,
      }
      path = os.path.join(os.path.dirname(__file__), 'main.html')
      page = template.render(path, data)
      memcache.add(key=hash, value=page , time=86400);
    self.response.out.write(page)

class OutPage(webapp.RequestHandler):
  def get(self, id):
    post = get_post(int(id));
    if (post):
      post.score = post.score + 1;
      post.put()
      self.redirect(post.url);
    else:
      self.redirect('/');

class SearchPage(webapp.RequestHandler):
  def get(self):
    data = {
      'mainid': 0,
      'subid': 0,
      'title': "Търсене &raquo; Безплатно е!",
      'maincat' : get_all_main(),
      'content': "templates/search.html",
    }
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, data))

class ForumPage(webapp.RequestHandler):
  def get(self):
    data = {
      'mainid': 0,
      'subid': 0,
      'title': "Форум &raquo; Безплатно е!",
      'maincat' : get_all_main(),
      'content': "templates/forum.html",
    }
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, data))

class RssPage(webapp.RequestHandler):
  def get(self):
    q = Item.all().order('-created')
    data = {
      'title': "Безплатно е!",
      'items': q.fetch(30),
      'last_updated': datetime.datetime.now(),
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/feed.xml')
    self.response.out.write(template.render(path, data))

class VotePage(webapp.RequestHandler):
  def post(self):
    ip = self.request.remote_addr;
    score = vote(ip, self.request);
    self.response.out.write('Рейтинг: '+str(score))

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/c/(\d+)/([\w\-]+)', CategoryPage),
                                      ('/sub/(\d+)/([\w\-]+)/([\w\-]+)', SubCategoryPage),
                                      ('/post/(\d+)/([\w\-]+)', PostPage),
                                      ('/out/(\d+)', OutPage),
                                      ('/search', SearchPage),
                                      ('/forum', ForumPage),
                                      ('/feed', RssPage),
                                      ('/vote', VotePage),
                                      ],
                                     debug=False)

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
