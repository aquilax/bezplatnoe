# -*- encoding: utf-8 -*-

__author__="aquilax"
__date__ ="$Sep 21, 2010 6:41:02 PM$"

from google.appengine.ext import db
from google.appengine.api import memcache
import htmlentitydefs, re
from slugify import slughifi

class MainCategory(db.Model):
  name = db.StringProperty(verbose_name="Name")
  slug = db.StringProperty(verbose_name="Slug")
  created = db.DateTimeProperty(verbose_name="Addred", auto_now_add=True)

class SubCategory(db.Model):
  main = db.ReferenceProperty(MainCategory)
  name = db.StringProperty(verbose_name="Name")
  slug = db.StringProperty(verbose_name="Slug")
  created = db.DateTimeProperty(verbose_name="Addred", auto_now_add=True)

class Item(db.Model):
  main = db.ReferenceProperty(MainCategory)
  sub = db.ReferenceProperty(SubCategory)
  title = db.StringProperty(verbose_name="Title")
  slug = db.StringProperty(verbose_name="Slug")
  text = db.TextProperty(verbose_name="Text")
  image = db.StringProperty(verbose_name="Image")
  url = db.StringProperty(verbose_name="URL")
  keywords = db.StringProperty(verbose_name="Keywords")
  created = db.DateTimeProperty(verbose_name="Addred", auto_now_add=True)
  score = db.IntegerProperty(default=1)

def get_all_main():
  hash = 'mc:'
  items = memcache.get(hash)
  if (not items):
    mc = MainCategory.all().order('name')
    items = mc.fetch(100)
    memcache.add(key=hash, value=items , time=86400);
  return items

def get_main(id):
  return MainCategory.get_by_id(id)

def get_sub(id):
  return SubCategory.get_by_id(id)

def get_post(id):
  return Item.get_by_id(id)


def create_slug(text, separator = '-'):
  text = slughifi(text)
  ret = ""
  for c in text.lower():
    try:
      ret += htmlentitydefs.codepoint2name[ord(c)]
    except:
      ret += c

  ret = re.sub("([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)", r"\1", ret)
  ret = re.sub("\W", " ", ret)
  ret = re.sub(" +", separator, ret)

  return ret.strip()

def save_category(data):
  id = int(data.get('main_id'))
  main_name = data.get('main_name')
  sub_name = data.get('sub_name')
  if (id != 0):
    main = get_main(id)
  else:
    main = MainCategory();
    main.name = main_name
    main.slug = create_slug(main_name)
    main.put()
  subcat = SubCategory();
  subcat.main = main
  subcat.name = sub_name
  subcat.slug = create_slug(sub_name)
  subcat.put();

def save_post(data):
  subcat_id = int(data.get('subcat'))
  title = data.get('title')
  image = data.get('image')
  url = data.get('url')
  text = data.get('text')
  keywords = data.get('keywords')
  sub = get_sub(subcat_id)
  item = Item()
  item.main = sub.main
  item.sub = sub
  item.title = title
  item.slug = create_slug(title)
  item.image = image
  item.url = url
  item.text = text
  item.keywords = keywords
  item.put()

def update_post(id, data):
  subcat_id = int(data.get('subcat'))
  sub = get_sub(subcat_id)
  title = data.get('title')
  image = data.get('image')
  url = data.get('url')
  text = data.get('text')
  keywords = data.get('keywords')
  item = get_post(id);
  item.main = sub.main
  item.sub = sub
  item.title = title
  item.slug = create_slug(title)
  item.image = image
  item.url = url
  item.text = text
  item.keywords = keywords
  item.put()

def vote(ip, data):
  id = data.get('id')
  item = get_post(int(id))
  if (item):
    hash = id+'_'+ip;
    voted = memcache.get(hash)
    if (not voted):
      if (int(data.get('action')) == 1):
        item.score = item.score + 10;
      else:
        item.score = item.score - 10;
      item.put()
      memcache.add(key=hash, value=1, time=86400);
    return item.score
  return 0