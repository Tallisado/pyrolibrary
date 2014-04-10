import os
from keywords import *

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION

class PyroLibrary( 
    _BrowserManagementKeywords
):

    """PyroLibrary is a web testing wrapper for the Selnium2Library library in Robot Framework.
    See https://github.com/rtomac/robotframework-selenium2library
    
    It uses the Selenium 2 (WebDriver) libraries internally to control a web browser.
    See http://seleniumhq.org/docs/03_webdriver.html for more information on Selenium 2
    and WebDriver.

    PyroLibrary runs tests in a real browser instance. It should work in
    most modern browsers and can be used with both Python and Jython interpreters.

    PyroLibrary adds functionality to run remote browsers under the Sauce services
    See https://saucelabs.com
    
    *Before running tests*

    Prior to running test cases using Selenium2Library and PyroLibrary, these libraries must be
    imported into your Robot test suite (see `importing` section), and the 
    `Open Browser` or `Open Pyro Browser` keyword must be used to open a browser to the desired location.

    *Locating elements*

    All keywords that need to find an element on the page
    take an argument, `locator`. By default, when a locator value is provided,
    it is matched against the key attributes of the particular element type.
    For example, `id` and `name` are key attributes to all elements, and
    locating elements is easy using just the `id` as a `locator`. For example::

    Click Element  my_element

    It is also possible to specify the approach Selenium2Library should take
    to find an element by specifying a lookup strategy with a locator
    prefix. Supported strategies are:

    | *Strategy* | *Example*                               | *Description*                                   |
    | identifier | Click Element `|` identifier=my_element | Matches by @id or @name attribute               |
    | id         | Click Element `|` id=my_element         | Matches by @id attribute                        |
    | name       | Click Element `|` name=my_element       | Matches by @name attribute                      |
    | xpath      | Click Element `|` xpath=//div[@id='my_element'] | Matches with arbitrary XPath expression |
    | dom        | Click Element `|` dom=document.images[56] | Matches with arbitrary DOM express            |
    | link       | Click Element `|` link=My Link          | Matches anchor elements by their link text      |
    | css        | Click Element `|` css=div.my_class      | Matches by CSS selector                         |
    | jquery     | Click Element `|` jquery=div.my_class   | Matches by jQuery/sizzle selector                         |
    | sizzle     | Click Element `|` sizzle=div.my_class   | Matches by jQuery/sizzle selector                         |
    | tag        | Click Element `|` tag=div               | Matches by HTML tag name                        |

    Table related keywords, such as `Table Should Contain`, work differently.
    By default, when a table locator value is provided, it will search for
    a table with the specified `id` attribute. For example:

    Table Should Contain  my_table  text

    More complex table lookup strategies are also supported:

    | *Strategy* | *Example*                                                          | *Description*                     |
    | css        | Table Should Contain `|` css=table.my_class `|` text               | Matches by @id or @name attribute |
    | xpath      | Table Should Contain `|` xpath=//table/[@name="my_table"] `|` text | Matches by @id or @name attribute |

    *Timeouts*

    There are several `Wait ...` keywords that take timeout as an
    argument. All of these timeout arguments are optional. The timeout
    used by all of them can be set globally using the
    `Set Selenium Timeout` keyword.

    All timeouts can be given as numbers considered seconds (e.g. 0.5 or 42)
    or in Robot Framework's time syntax (e.g. '1.5 seconds' or '1 min 30 s').
    For more information about the time syntax see:
    http://robotframework.googlecode.com/svn/trunk/doc/userguide/RobotFrameworkUserGuide.html#time-format.    
    def __init__(self):
        for base in PyroLibrary.__bases__:
            base.__init__(self)
        # self.set_selenium_timeout(timeout)
        # self.set_selenium_implicit_wait(implicit_wait)
        # self.register_keyword_to_run_on_failure(run_on_failure)
    """