# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def index():
    #form = db(db.our_to_do_list.Author == db.auth_user.first_name).select(db.our_to_do_list.ALL)
    query = (db.our_to_do_list.Author == auth.user_id)
    form = SQLFORM.grid(query)
    query_one = (db.assigned_to_others.Assignee == auth.first_name)
    form = SQLFORM.grid(query_one)   
    query_two = (db.assigned_to_others.Author == auth.user_id)
    form_two = SQLFORM.grid(query_two)
    #db(db.assigned_to_others.Author == db.auth_user.first_name).select(db.assigned_to_others.ALL)
    return dict(form=form, form_two = form_two)

def add():
    form = SQLFORM(db.our_to_do_list, requires = IS_NOT_EMPTY)
    if form.process().accepted:
        session.flash = 'Task assigned to self'
        redirect('index')
    return dict(form = form)

def add_other():
    form = SQLFORM(db.assigned_to_others, requires = IS_NOT_EMPTY)
    if form.process().accepted:
        session.flash = 'Task assigned to other'
        redirect('index')
    return dict(form = form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
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


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
