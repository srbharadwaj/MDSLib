from .interface import Interface
from .constants import SHUTDOWN,NO_SHUTDOWN
import logging

log = logging.getLogger(__name__)


class Fc(Interface):

    def __init__(self, switch, name):
        super().__init__(switch, name)
        self.__swobj = switch

    # property for out_of_service
    def _set_out_of_service(self, value):
        cmd = "terminal dont-ask ; interface " + self.name + " ; out-of-service force ; no terminal dont-ask "
        if value:
            self.status = SHUTDOWN
        else:
            self.status = NO_SHUTDOWN
            cmd = cmd.replace("out-of-service", "no out-of-service")
        self.__swobj.config(cmd)

    # out_of_service property
    out_of_service = property(fset=_set_out_of_service)
