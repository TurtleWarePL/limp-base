from evennia import Command

class CmdPhone(Command):
    """
    Call a phone of a given number.

    Usage:
      phone [number]
      call [number]
    """
    key = "phone"

    aliases = ["call"]
    
    def func(self):
        from typeclasses.phones import Phone
        caller = self.caller
        location = caller.location

        if not self.args:
            caller.msg("Usage: phone [number].")
        else:
            target_phone = Phone.find_phone(int(self.args))
            # Echo the ringing to every object in the -room- (not location) the phone is in.
            target_phone.which_room().msg_contents("{} rings!".format(target_phone.name).capitalize())



from evennia import CmdSet
from evennia import default_cmds

class PhoneCmdSet(CmdSet):
    key = "phonecmdset"

    def at_cmdset_creation(self):
        self.add(CmdPhone())
