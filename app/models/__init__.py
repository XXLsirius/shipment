from .Ship import Ship
from .Waterarea import Waterarea
from .Mariner import Mariner
from .Charterer import Charterer
from .Certtype import Certtype
from .Certificate import Certificate
import os
__all__ = ["Ship", "Waterarea", "Mariner", "Charterer", "Certtype", "Certificate"]

os.environ['REDIS_OM_URL'] = 'redis://@192.168.140.211:6379'

Charterer.init()
Waterarea.init()
Certificate.init()
Mariner.init()
Certtype.init()
Ship.init()
