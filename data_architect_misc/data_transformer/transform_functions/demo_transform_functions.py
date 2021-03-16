"""
This transform function is to demo certain capabilities of functions
implemented in this transform module.
"""

import logging
import re

import pandas as pd

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class DemoTransformFunctions(CommonCompHarmTransformFunctions):

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
