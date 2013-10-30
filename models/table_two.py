# coding: utf8

db.define_table('assigned_to_others',
                Field('Author', 'string', default = auth.user_id),
                Field('Assignee', 'string'),
                Field('Title', 'string'),
                Field('ToDo', 'text')
)

db.assigned_to_others.Author.writable = db.assigned_to_others.Author.readable = False
