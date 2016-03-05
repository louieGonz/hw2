# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

# voting example in web2py
from datetime import datetime

db = DAL("sqlite://storage.sqlite")

# will require a login to add to the table
from gluon.tools import Auth

auth = Auth(db)
auth.define_tables(username=False, signature=False)

db.define_table('seller',
                Field('name'),
                Field('rating', 'integer', default=0)
                )
#only autofill if signed in
if auth.user:
    db.seller.name.default = auth.user.first_name
    db.seller.name.writable = False




# table defintion for all info of a post
db.define_table('posts',
                Field('name'),
                Field('seller_ref','reference seller'),
                Field('email'),
                Field('phone'),
                Field('date_posted', 'datetime'),
                Field('title', unique=True),
                Field('description'),
                Field('listing_category'),
                Field('price', 'double'),
                Field('listing_status', 'boolean'),
                format='%(title)s')


# validators for the table
db.posts.date_posted.default = datetime.utcnow()
db.posts.seller_ref.writable = False
db.posts.seller_ref.readable = False
#db.posts.name.default = db.seller.name
db.posts.date_posted.writable = False
db.posts.title.requires = IS_NOT_IN_DB(db, db.posts.title) #need unique titles
db.posts.price.require = IS_FLOAT_IN_RANGE(0, 100000.0, dot=".",
                                           error_message='the price should be in the range 0 ... 100000.0')

db.posts.email.requires = IS_EMAIL()
db.posts.phone.default = '1-'
# will require that the phone number is valid
db.posts.phone.requires = IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$',
                                   error_message='not a phone number')

#
db.posts._singular = "Posts"
db.posts._plural = "Posts"

# so that grid will not diplay posts id
db.posts.id.readable = False


db.define_table('images',
                Field('image', 'upload'),
                Field('description','reference posts')
                )


db.images.description.writable = False
db.images._singular = "Image"
db.images._plural = "Images"
db.images.id.readable = False