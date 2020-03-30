class CommonException(Exception):
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


class UnsupportedVersion(CommonException):
    pass


# zone related exceptions
class InvalidZoneMode(CommonException):
    pass


class InvalidZoneMemberType(CommonException):
    pass


class VsanNotPresent(CommonException):
    pass


# interface related exceptions
class InvalidInterface(CommonException):
    pass


class InvalidStatus(CommonException):
    pass


class InvalidTrunkMode(CommonException):
    pass


class InvalidSpeed(CommonException):
    pass


class InvalidMode(CommonException):
    pass


# portchannel related exceptions
class PortChannelNotPresent(CommonException):
    pass


class InvalidPortChannelRange(CommonException):
    pass

class InvalidChannelMode(CommonException):
    pass

class ZoneNotPresent(CommonException):
    pass


# Analytics related exceptions
class InvalidAnalyticsType(CommonException):
    pass


class InvalidProfile(CommonException):
    pass
