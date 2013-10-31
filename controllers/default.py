# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
def get_first_email():
    if auth.user:
        return auth.user.email
    else:
        return 'anonymous'


@auth.requires_login()
def index(): 
    query = (db.our_to_do_list.Author == get_first_email)
    form = SQLFORM.grid(query,
    searchable = False, create = False, editable = False, csv = False)
    query_one = (db.assigned_to_others.Assignees_Email == auth.user.email)
    form_one = SQLFORM.grid(query_one,
    searchable = False, create = False, editable = False,  csv = False, links=[
    dict(header=T('Accepted?'),
          body = lambda r: r.Task_Accepted), # displays False all the time),
        ])
    query_two = (db.assigned_to_others.Author == auth.user.email)
    form_two = SQLFORM.grid(query_two,
    searchable = False, create = False, editable = False, csv = False)
    return dict(form=form, form_two = form_two, form_one = form_one)


def accept_task():
    form = SQLFORM(db.assigned_to_others)
    if form.process().on_click:
        if form.vars.Assignee == get_first_email:
            my_record = db.assigned_to_others(db.assigned_to_others.id == form.vars.id)
            my_record.update_record(Task_Accepted=True)
            session.flash=T(str(form.vars.Task_Accepted))
    redirect(URL('default', 'index'))

def add():
    form = SQLFORM(db.our_to_do_list, requires = IS_NOT_EMPTY)
    if form.process().accepted:
        session.flash = 'Task assigned to self'
        redirect('index')
    return dict(form = form)

def Assign_to_other():
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
