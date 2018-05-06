from typeclasses.objects import Object
from random import randint
from commands.phonecmd import PhoneCmdSet

class Phone(Object):
    used_numbers = {}

    @staticmethod
    def find_phone(number):
        if number in Phone.used_numbers:
            return Phone.used_numbers[number]
        else:
            return None

    def at_object_creation(self):
        #TODO: make sure two phones can't have identical numbers
        self.db.number = randint(100000000,999999999)
        self.update_desc()
        self.cmdset.add(PhoneCmdSet, permanent=True)
        self.locks.add("puppet:false()")
        self.add_to_list()
        #self.db.connection = None

    #TODO: can we somehow generate it dynamically rather than always call update?
    def update_desc(self):
        self.db.desc = "A black smartphone.\n\n" + str(self.db.number)

    def at_object_delete(self):
        del self.used_numbers[self.db.number]
        return True

    def at_init(self):
        self.add_to_list()
        self.connection = None

    def add_to_list(self):
        self.used_numbers[self.db.number] = self
