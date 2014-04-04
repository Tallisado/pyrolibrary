import os
import sys

# sauce rest api
import re
import requests

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem
from sauce_rest import *

# envname_pyrobot_browser = 'PYROBOT_BROWSER'
# envname_pyrobot_default_browser = "PYROBOT_DEFAULT_BROWSER"

VERSION = "v1.1"

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

seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
job_id = ""
print "pybotLibrary %s" % VERSION

def open_browser_login_sencha(_username, _password, _element_on_next_page, _browser=os.environ.get("PYBROWSER", 'firefox')):
    #seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    if os.environ.get("PYBROWSER", "0") == "0":
        #sauce
        seleniumlib.open_browser(os.environ['BASE_URL'], browser=_browser, remote_url=os.environ["PYROBOT_REMOTE_URL"], desired_capabilities=os.environ["PYROBOT_CAPS"])        
    else:
        #local solo
        seleniumlib.open_browser(os.environ['BASE_URL'], browser=_browser) 
    job_id = seleniumlib._current_browser().session_id    
    print "dump pyro_jobid"
    if os.environ.get('SAUCE_API_KEY') and os.environ.get('SAUCE_USERNAME'):
        wrapper = Wrapper(seleniumlib, os.environ.get('SAUCE_USERNAME'), os.environ.get('SAUCE_API_KEY'), sys.argv[2])
        wrapper.dump_session_id()
        
    ondemand_string = "SauceOnDemandSessionID=%s job-name=%s" % (job_id, BuiltIn().get_variable_value("${SUITE_NAME}"))
    print 'setting ONDEMAND_PYRO to : %s' % ondemand_string
    OperatingSystem().set_environment_variable("ONDEMAND_PYRO", "1111")    
    os.environ['ONDEMAND_PYRO'] = ondemand_string
        
    seleniumlib.maximize_browser_window()
    seleniumlib.set_selenium_speed(1)
    seleniumlib.wait_until_element_is_visible('loginnameid-inputEl', timeout=5)
    seleniumlib.wait_until_element_is_visible('loginpasswordid-inputEl', timeout=5)
    seleniumlib.input_text('loginnameid-inputEl', _username)
    seleniumlib.input_text('loginpasswordid-inputEl', _password)
    seleniumlib.wait_until_element_is_visible('loginbuttonid-btnIconEl', timeout=5)
    seleniumlib.click_element('id=loginbuttonid-btnIconEl')
    seleniumlib.wait_until_element_is_visible('id=%s'% _element_on_next_page, timeout=5)


def tallis_keyword(): 
   print 'CLOSE BROWSER TIME'
   
def close_pyro_browser():
    print 'CLOSE BROWSER TIME'
    # sauce enabled
    #seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    if os.environ.get("PYBROWSER", "0") == "0":
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
        url = 'https://saucelabs.com/rest/v1/{0}/jobs/{1}'.format(username, job_id)
        response = requests.put(url, data=json.dumps(payload), headers=headers)
        assert response.status_code == 200, response.text
        # video_url = json.loads(response.text).get('video_url')
        # if video_url:
            # logger.info('<a href="{0}">video.flv</a>'.format(video_url), html=True)
        ondemand_string = "SauceOnDemandSessionID=%s job-name=%s" % (job_id, suite_name)
        print 'setting ONDEMAND_PYRO to : %s' % ondemand_string    
        os.environ['ONDEMAND_PYRO'] = ondemand_string
        #wrapper = Wrapper(seleniumlib, username, access_key, sys.argv[2])
        #wrapper.update_sauce_rest(BuiltIn().get_variable_value("${SUITE STATUS}"), BuiltIn().get_variable_value("${TEST_TAGS}"))
    
    seleniumlib.close_browser
    seleniumlib.close_all_browsers
    print 'CLOSE BROWSER TIME!!'