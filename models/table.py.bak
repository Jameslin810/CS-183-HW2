# coding: utf8
def get_first_name():
    if auth.user:
        return auth.user.first_name
    else:
        return 'anonymous'


db.define_table('our_to_do_list',
                Field('Author', 'string', default = get_first_name),
                Field('Title', 'string'),
                Field('ToDo', 'text')
)


#db.our_to_do_list.Author.writable = db.our_to_do_list.Author.readable = False
db.our_to_do_list.Author.writable = False
