class User:
    """Gebruikers van MobileCare"""

    def __init__(self, id, first, last, age, email):
        self.first = first
        self.last = last
        self.age = age
        self.id = id
   

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

#    @property
#    def fullname(self):
#        return '{} {}'.format(self.first, self.last)

#    @fullname.setter
#    def fullname(self, name):
#        first, last = name.split('')
#        self.first = first
#        self.last = last

#    @fullname.deleter
#    def fullname(self):
#        print('Delete Name!')
#        self.first = None
#        self.last = None

#    def __repr__(self):
#        return "User('{}', '{}', '{}')".format(self.first, self.last)