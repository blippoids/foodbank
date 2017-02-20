# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

try: db = DAL(os.environ.get('DATABASE_URL'))
except: db = DAL('sqlite://storage.sqlite')


# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db)
auth.define_tables(username=False,signature=False)
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------

db.define_table("category",
                Field("name", "string"),
                Field("created", "date"),
                format='%(name)s',
                )

db.define_table("unit",
                Field("name", "string"),
                Field("created", "date"),
                format='%(name)s',
                )

db.define_table("location",
                Field("town", "string"),
                Field("city", "string"),
                Field("countrycode", "string"),
                Field("country", "string"),
                Field("longitude", "float"),
                Field("latitude", "float"),
                Field("street", "string"),
                Field("post_code", "string"),
                Field("post_code_prefix", "string"),
                format="%(city)s")

db.define_table("volunteer",
                Field("volunteer_id", "string"),
                Field("first_name", "string"),
                Field("last_name", "string"),
                Field("joined", "date"),
                Field("address", "string"),
                Field("roles", "string"),
                Field("thumbnail", "text"),
                Field("public_location", "reference location"),
                Field("biography", "text"),
                Field("thumbnail", "string"),
                format='%(first_name)s'
                )

db.define_table("retailer",
                Field("name", "string"),
                Field("join_date", "date"),
                Field("address", "string"),
                format="%(name)s",
                )

db.define_table("entrance",
                Field("date", "date"),
                Field("from_retailer", 'reference retailer'),
                Field("from_volunteer", 'reference volunteer'),
                format=lambda r: '%s: %s-%s' % (r.date, r.from_retailer.name, r.from_volunteer.name),
                )


db.define_table("product",
                Field("amount", "double"),
                Field('unit', 'reference unit', required=False),
                Field('from_category', 'reference category', required=False),
                Field('from_entrance', 'reference entrance', required=False),
                format="%(from_category)s-%(from_entrance)s",
                )

db.define_table("project",
                Field("project_id", "text"), ## add more
                format="%(project_id)s"
                )

db.define_table("event",
                Field("event_id", "text"),
                Field("name", "text"),
                Field("description", "text"),
                Field("organiser_id", "text"),
                Field("end_date_time", "text"),
                Field("status", "integer"),
                Field("location_id", "reference location"),
                format="%(name)s"
                )

db.define_table("event_volunteer",
                Field("event_id", "reference_event"),
                Field("volunteer_id", "reference volunteer"),
                format='%(id)s')

auth.enable_record_versioning(db)
