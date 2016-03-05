# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    # post posts table to grid
    # require person to log in to edit and add, by settin user_signature = True
    grid = SQLFORM.smartgrid(db.posts,linked_tables=['images'],user_signature=True,csv=False)
    return locals()
    #grid2 = SQLFORM.grid(db.images,user_signature=True)
    #return dict(grid=grid,grid2=grid2)

######################################################################
# jquery controllers

def list_sellers():
    items = db().select(db.seller.ALL, orderby=db.seller.rating)
    return dict(items=items)

def vote():
    item = db.seller[request.vars.id]
    new_votes = item.rating + 1
    item.update_record(rating=new_votes)
    return str(new_votes)

#######################################################################
def imageView():
    #stores images database in var tables

    tables = db.images

    descriptions = tables.description


    #stores a field in variable image
    images = tables.image
    #gets a record of images

    s = db(images)
    t = db(descriptions)

    #creates iterable object from record
    rows = s.select()
    rows2 = t.select()

    deadbeef = db(db.images.id).select()
    aha = db(db.images.description).select()
    return dict(aha=aha,t=t,tables=tables,images=images,descriptions=descriptions,s=s,rows=rows,rows2=rows2,deadbeef=deadbeef)


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
