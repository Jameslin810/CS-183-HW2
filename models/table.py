# coding: utf8


db.define_table('our_to_do_list', 
                Field('Author', 'string', default = auth.user_id),
                Field('Title', 'string'),
                Field('ToDo', 'text')
)


db.our_to_do_list.Author.writable = db.our_to_do_list.Author.readable = False
