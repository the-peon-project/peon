import logging
import discord
from typing import List, Optional
from . import *
from .orchestrator import *
from .shared import *

# NOTE: this module used to define `PersistentAdministratorView`, an empty
# placeholder (no buttons, not correctly configured for persistence either)
# that achieved nothing when registered, so it was deleted rather than
# patched. main.py's /peon admin-mode branch used to construct a
# corresponding `EnhancedAdministratorView()` that was never defined anywhere
# in the codebase (a NameError on every use) -- that branch now sends its
# embed without a view instead, until a real admin button panel is designed.
