import os
from keywords import *

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION

class PyroLibrary( 
    _BrowserManagementKeywords
):

    def __init__(self):
        for base in Selenium2Library.__bases__:
            base.__init__(self)
        # self.set_selenium_timeout(timeout)
        # self.set_selenium_implicit_wait(implicit_wait)
        # self.register_keyword_to_run_on_failure(run_on_failure)
