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
        if self.obj.connection is None:
            from typeclasses.phones import Phone
            caller = self.caller
            location = caller.location

            if not self.args:
                caller.msg("Usage: phone [number].")
            else:
                target_phone = Phone.find_phone(int(self.args))
                # Echo the ringing to every object in the -room- (not location) the phone is in.
                target_phone.which_room().msg_contents("{} rings!".format(target_phone.name).capitalize())
                target_phone.connection = self.obj
                self.obj.connection = target_phone
        else:
            self.caller.msg("You are already in call.")

class CmdHangup(Command):
    """
    Hang up during an ongoing call.

    Usage:
      hangup
    """

    key = "hangup"

    def func(self):
        if self.obj.connection is None:
            self.caller.msg("You are not currently calling anyone.")
        else:
            self.caller.msg("You hang up.")
            self.obj.connection.location.msg("The call ends.")
            self.obj.connection.connection = None
            self.obj.connection = None

class CmdTalk(Command):
    """
    Talk over the phone.
    
    Usage:
      talk [message]
    """

    key = "talk"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage: talk [message]")
        elif self.obj.connection is None:
            caller.msg("You're not calling anyone.")
        else:
            target_phone = self.obj.connection
            target_phone.location.msg("A voice speaks from the phone, \"{}\"".format(self.args.strip()))
            caller.msg("You speak into the phone, \"{}\"".format(self.args.strip()))



from evennia import CmdSet
from evennia import default_cmds

class PhoneCmdSet(CmdSet):
    key = "phonecmdset"

    def at_cmdset_creation(self):
        self.add(CmdPhone())
        self.add(CmdHangup())
        self.add(CmdTalk())
