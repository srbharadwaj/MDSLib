import re

from mdslib.constants import PAT_WWN


def is_pwwn_valid(pwwn):
    newpwwn = pwwn.lower()
    match = re.match(PAT_WWN, newpwwn)
    if match:
        return True
    return False
