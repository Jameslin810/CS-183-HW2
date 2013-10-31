# coding: utf8

def get_first_name():
    if auth.user:
        return auth.user.first_name
    else:
        return 'anonymous'

db.define_table('assigned_to_others',
                Field('Author', 'string', default = get_first_name),
                Field('Assignee', 'string'),
                Field('Title', 'string'),
                Field('ToDo', 'text')
)

db.assigned_to_others.Author.writable = False
