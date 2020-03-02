# -*- coding: utf-8 -*-
"""CrowdStrike client library."""

import logging

from .__version__ import __description__, __title__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__


# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "__description__",
    "__title__",
    "__url__",
    "__version__",
    "__author__",
    "__author_email__",
    "__license__",
    "__copyright__",
]
