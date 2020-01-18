import logging
from .connection_manager.errors import CLIError
from . import constants

log = logging.getLogger(__name__)


class InvalidArgument(Exception):
    """

    """

    def __init__(self, message):
        """

        Args:
            message:
        """
        self.message = message.strip()

    def __repr__(self):
        """

        Returns:

        """
        return '%s: %s' % (self.__class__.__name__, self.message)

    __str__ = __repr__


class DeviceAlias(object):
    def __init__(self, sw):
        self.__swobj = sw

    @property
    def mode(self):
        facts_out = self.__get_facts()
        return self.__get_mode(facts_out)

    @mode.setter
    def mode(self, mode):
        log.debug("Setting device alias mode to " + mode)
        if mode.lower() == constants.ENHANCED:
            cmd = "device-alias database ; device-alias mode enhanced"
        elif mode.lower() == constants.BASIC:
            cmd = "device-alias database ; no device-alias mode enhanced"
        else:
            raise InvalidArgument("Invalid device alias mode: " + str(
                mode) + ". Valid values are " + constants.ENHANCED + "," + constants.BASIC)
        self.__send_device_alias_cmds(cmd)

    @property
    def distribute(self):
        facts_out = self.__get_facts()
        dis = self.__get_distribute(facts_out)
        if dis.lower() == 'enabled':
            return True
        else:
            return False

    @distribute.setter
    def distribute(self, distribute):
        if distribute:
            cmd = "device-alias database ; device-alias distribute"
            log.debug("Setting device alias mode to 'Enabled'")
            log.debug(cmd)
        else:
            cmd = "device-alias database ; no device-alias distribute"
            log.debug("Setting device alias mode to 'Disabled'")
            log.debug(cmd)
        self.__send_device_alias_cmds(cmd)

    @property
    def locked(self):
        facts_out = self.__get_facts()
        if self.__locked_user(facts_out) is None:
            return False
        return True

    @property
    def database(self):
        retout = {}
        facts_out = self.__get_facts()
        allentries = facts_out.get('device_alias_entries', None)
        if allentries is None:
            return None
        else:
            if type(allentries) is dict:
                # That means there is only one entry in the database
                allentries = [allentries]
            for eachentry in allentries:
                retout[eachentry['dev_alias_name']] = eachentry['pwwn']
            return retout

    def create(self, namepwwn):
        existingdb = self.database
        cmd = "device-alias database ; "
        facts_out = self.__get_facts()
        mode = self.mode
        for name, pwwn in namepwwn.items():
            if existingdb and name in existingdb:
                log.error("Device alias name " + name + " is already present in the database")
                continue
            if existingdb and pwwn in existingdb.values():
                log.error("pwwn " + pwwn + " already present in the database with another name")
                continue
            log.info("Creating device alias with name:pwwn  " + name + " : " + pwwn)
            cmd = "device-alias database ; "
            cmd = cmd + " device-alias name " + name + " pwwn " + pwwn + " ; "
            self.__send_device_alias_cmds(cmd, facts_out, mode, skipcommit=True)
        dist = self.distribute
        if dist and dist is not None:
            self.__send_commit(mode)

    def delete(self, name):
        existingdb = self.database
        if existingdb:
            if name not in existingdb:
                log.info("Device alias name " + name + " doesnt not exist in the database, hence cannot be deleted")
            else:
                log.debug("Deleting device alias with args " + name)
                cmd = "device-alias database ; no device-alias name " + name
                self.__send_device_alias_cmds(cmd)
        else:
            log.error("There are no device alias entries in the database, hence there is nothing to delete")

    def rename(self, oldname, newname):
        existingdb = self.database
        if existingdb:
            if oldname not in existingdb:
                log.error("Device alias name " + oldname + " cannot be renamed as it does not exist in the database")
            elif newname in existingdb:
                log.error(
                    "Device alias name " + newname + " is already present in the database, hence '" + oldname + "' cannot be renamed to '" + newname + "'")
            else:
                log.debug("Renaming device alias with args " + oldname + " " + newname)
                cmd = "device-alias database ; device-alias rename " + oldname + " " + newname
                self.__send_device_alias_cmds(cmd)
        else:
            log.error("There are no device alias entries in the database, hence there is nothing to rename")

    def clear_lock(self):
        log.info("Sending the cmd clear device-alias session")
        cmd = "terminal dont-ask ; device-alias database ; clear device-alias session ; no terminal dont-ask "
        self.__swobj.config(cmd)

    def __get_facts(self):
        log.debug("Getting device alias facts")
        retoutput = {}
        out = self.__swobj.show("show device-alias database")
        if out:
            num = out['number_of_entries']
            da = out['TABLE_device_alias_database']['ROW_device_alias_database']

            retoutput['number_of_entries'] = num
            retoutput['device_alias_entries'] = da
        shdastatus = self.__swobj.show("show device-alias status")

        return dict(retoutput, **shdastatus)

    def clear_database(self):
        log.info("Sending the cmd clear device-alias database")
        cmd = "terminal dont-ask ; device-alias database ; clear device-alias database ; no terminal dont-ask "
        self.__send_device_alias_cmds(cmd)

    @staticmethod
    def __get_mode(facts_out):
        return facts_out['database_mode']

    @staticmethod
    def __get_distribute(facts_out):
        return facts_out['fabric_distribution']

    @staticmethod
    def __locked_user(facts_out):
        if 'Locked_by_user' in facts_out.keys():
            log.debug(facts_out['Locked_by_user'])
            return facts_out['Locked_by_user']
        else:
            return None

    def __send_device_alias_cmds(self, command, facts_out=None, mode=None, skipcommit=False):
        if facts_out is None:
            facts_out = self.__get_facts()
        if mode is None:
            mode = self.mode

        if 'distribute' in command:
            dist = None
        else:
            dist = self.distribute
        log.debug("mode is " + mode)
        log.debug("distribute is " + str(dist))
        lock_user = self.__locked_user(facts_out)
        if lock_user is not None:
            log.error("Switch has acquired cfs device-alias lock by user " + lock_user)
            self.__clear_lock_if_enhanced(mode)
            raise CLIError(command, "Switch has acquired cfs device-alias lock by user " + lock_user)

        log.debug("Sending the command..")
        log.debug(command)
        out = self.__swobj.config(command)
        if out is not None:
            msg = out['msg']
            if "Device Alias already present" in msg:
                log.info("The command : " + command + " was not executed because Device Alias already present")
                self.__clear_lock_if_enhanced(mode)
            else:
                log.error(msg)
                self.__clear_lock_if_enhanced(mode)
                raise CLIError(command, msg)

        if skipcommit:
            return False, None
        else:
            if dist and dist is not None:
                self.__send_commit(mode)

    def __send_commit(self, mode):
        cmd = "terminal dont-ask ; device-alias commit ; no terminal dont-ask "
        log.debug(cmd)
        out = self.__swobj.config(cmd)
        if out is not None:
            if out['msg'].find("Device-alias enhanced zone member present"):
                log.error("Device-alias enhanced zone member present")
                self.__clear_lock_if_enhanced(mode)
                raise CLIError(cmd, out['msg'])

    def __clear_lock_if_enhanced(self, mode):
        if mode.lower() == constants.ENHANCED:
            self.clear_lock()
