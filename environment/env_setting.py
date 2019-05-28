# Standard library imports
from enum import Enum

# Third party imports

# Local application imports

class Host(Enum):
    HOME    = 1
    COMPANY = 2

ENVIRONMENT = Host.COMPANY