from PyroLibrary.utils import SauceRestWrapper
from keywordgroup import KeywordGroup
import os
import sys

# sauce rest api
import re
import requests

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem

USERNAME_ACCESS_KEY = re.compile('^(http|https):\/\/([^:]+):([^@]+)@')

SELENIUM2LIB_BROWSERS = [   
'ff',
'firefox',
'ie',
'internetexplorer',
'googlechrome',
'gc',
'chrome',
'opera',
'phantomjs',
'htmlunit',
'htmlunitwithjs',
'android',
'iphone',
'safari'                ]


class _BrowserManagementKeywords(KeywordGroup):

    def __init__(self):
        self._seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
        self._remoteBrowser = os.environ.get("PYBROWSER", "0") == "0"
        self._job_id = 0
        self._sauce_rest = SauceRestWrapper()
        
    def open_browser_login_sencha(self, user_name, password, element_on_next_page, determined_browser=os.environ.get("PYBROWSER", 'firefox')):
        print '(open_browser_login_sencha)'
        #self._seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
        if self._remoteBrowser: #sauce            
            self._seleniumlib.open_browser(os.environ['BASE_URL'], browser=determined_browser, remote_url=os.environ["PYROBOT_REMOTE_URL"], desired_capabilities=os.environ["PYROBOT_CAPS"])       
            self._job_id = self._seleniumlib._current_browser().session_id
        else:                   #local solo            
            self._seleniumlib.open_browser(os.environ['BASE_URL'], browser=determined_browser) 
            
        if os.environ.get('SAUCE_API_KEY') and os.environ.get('SAUCE_USERNAME') and self._remoteBrowser:
            print "execute sauce rest to update"
            self._sauce_rest.establish(self._seleniumlib._current_browser().session_id, os.environ.get('SAUCE_USERNAME'), os.environ.get('SAUCE_API_KEY'), sys.argv[2])
            self._sauce_rest.dump_session_id()
            #ondemand_string = "SauceOnDemandSessionID=%s job-name=%s" % (self._job_id, BuiltIn().get_variable_value("${SUITE_NAME}"))
            #print 'setting ONDEMAND_PYRO to : %s' % ondemand_string
            OperatingSystem().set_environment_variable("ONDEMAND_PYRO", "1111")    
            os.environ['ONDEMAND_PYRO'] = ondemand_string
                        
        self._seleniumlib.maximize_browser_window()
        self._seleniumlib.set_selenium_speed(1)
        self._seleniumlib.wait_until_element_is_visible('loginnameid-inputEl', timeout=5)
        self._seleniumlib.wait_until_element_is_visible('loginpasswordid-inputEl', timeout=5)
        self._seleniumlib.input_text('loginnameid-inputEl', user_name)
        self._seleniumlib.input_text('loginpasswordid-inputEl', password)
        self._seleniumlib.wait_until_element_is_visible('loginbuttonid-btnIconEl', timeout=5)
        self._seleniumlib.click_element('id=loginbuttonid-btnIconEl')
        self._seleniumlib.wait_until_element_is_visible('id=%s'% element_on_next_page, timeout=5)

    def close_pyro_browser():
        print '(close_pyro_browser)'
        # sauce enabled
        #self._seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
        if self._remoteBrowser:
            assert USERNAME_ACCESS_KEY.match(os.environ["PYROBOT_REMOTE_URL"]), 'Incomplete remote_url.'
            username, access_key = USERNAME_ACCESS_KEY.findall(os.environ["PYROBOT_REMOTE_URL"])[0][1:]
            suite_name = BuiltIn().get_variable_value("${SUITE_NAME}")
            suite_status = BuiltIn().get_variable_value("${SUITE STATUS}")
            tags = BuiltIn().get_variable_value("${TEST_TAGS}")
            
            print "name: %s status: %s tags: %s" % (suite_name, suite_status, tags)
            
            token = (':'.join([username, access_key])).encode('base64').strip()
            payload = { 'name': suite_name,
                        'passed': suite_status == 'PASS',
                        'tags': tags}
            headers = {'Authorization': 'Basic {0}'.format(token)}
            url = 'https://saucelabs.com/rest/v1/{0}/jobs/{1}'.format(username, self._job_id)
            response = requests.put(url, data=json.dumps(payload), headers=headers)
            assert response.status_code == 200, response.text
            # video_url = json.loads(response.text).get('video_url')
            # if video_url:
                # logger.info('<a href="{0}">video.flv</a>'.format(video_url), html=True)
            ondemand_string = "SauceOnDemandSessionID=%s job-name=%s" % (self._job_id, suite_name)
            print 'setting ONDEMAND_PYRO to : %s' % ondemand_string    
            os.environ['ONDEMAND_PYRO'] = ondemand_string
            #wrapper = Wrapper(self._seleniumlib, username, access_key, sys.argv[2])
            #wrapper.update_sauce_rest(BuiltIn().get_variable_value("${SUITE STATUS}"), BuiltIn().get_variable_value("${TEST_TAGS}"))
        
        self._seleniumlib.close_browser
        self._seleniumlib.close_all_browsers
        print 'CLOSE BROWSER TIME!!'