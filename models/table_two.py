# coding: utf8

def get_first_email():
    if auth.user:
        return auth.user.email
    else:
        return 'anonymous'

db.define_table('assigned_to_others',
                Field('Author', 'string', default = get_first_email),
                Field('Assignees_Email', 'string'),
                Field('Task_Title', 'string'),
                Field('ToDo_Task', 'text'),
                Field('Task_Accepted', 'boolean', default = False),
                Field('Task_Rejected', 'boolean', default = False)
)

db.assigned_to_others.Author.writable = False

#
#if db.assigned_to_others.Author == get_first_email:
#    db.assigned_to_others.Task_Accepted.readable = db.assigned_to_others.Task_Accepted.writable = False
#    db.assigned_to_others.Task_Rejected.readable = db.assigned_to_others.Task_Rejected.writable = False
