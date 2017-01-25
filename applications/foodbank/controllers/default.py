# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import json

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    redirect('entrance')
    return dict(grid=SQLFORM.smartgrid(db.entrance, linked_tables=['product'], user_signature=False))

@auth.requires_login()
def category():
    return dict(grid=SQLFORM.grid(db.category, user_signature=False))


@auth.requires_login()
def unit():
    return dict(grid=SQLFORM.grid(db.unit, user_signature=False))

@auth.requires_login()
def retailer():
    return dict(grid=SQLFORM.grid(db.retailer, user_signature=False))

@auth.requires_login()
def view_entrance():
    entrance_id = request.args(0,cast=int)
    entrance = db.entrance(entrance_id)
    products = db.product(db.product.from_entrance==entrance_id).select()
    return locals()

@auth.requires_login()
def entrance():
    if 'view' in request.args:
        var = int(request.args[-1])
        t = db(db.entrance.id==var).select(db.entrance.id)[0].id
        db.product.from_entrance.readable = db.product.from_entrance.writable = False
        db.product.from_entrance.default = t
        form = SQLFORM(db.product).process()
        productos = db(db.product.from_entrance==var).select()
    entrance = SQLFORM.smartgrid(db.entrance, linked_tables=['product'], user_signature=False)
    return locals()


@auth.requires_login()
def volunteer():
    return dict(grid=SQLFORM.grid(db.volunteer, user_signature=False))


@auth.requires_login()
def product():
    return dict(grid=SQLFORM.smartgrid(db.product, linked_tables=['category'], user_signature=False))


@auth.requires_login()
def get_items():
    val = json.loads(request.vars.array)
    return db(db.product.from_entrance==int(val.from_entrance)).select()
    #return db(db.product.from_arrival==int(request.vars.from_arrival)).select().json()


@auth.requires_login()
def add_items():
    return dict(form=SQLFORM(db.product), arrival_id=request.vars.from_arrival)
