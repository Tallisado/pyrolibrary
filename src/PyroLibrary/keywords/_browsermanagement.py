from PyroLibrary.utils import SauceRestWrapper
from keywordgroup import KeywordGroup
import os
import sys

#BROWSER='Linux,chrome,33 BASE_URL=http://admin:password@10.10.9.164:81 PAYLOAD=dev/sauce_ui python pyrobot.py

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
    def __init__(self, no_base=False):      
        self._remoteBrowser = os.environ.get("PYBROWSER", "0") == "0"
        self._job_id = 0
        self._sauce_rest = SauceRestWrapper()
        if no_base:
            self._seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
       
    def open_pyro_browser(self, determined_browser=os.environ.get("PYBROWSER", 'firefox'), selenium_speed=1):
        """Opens a browser in the context determined by the suite; such as, Sauce Miltiple, Sauce Single, Sauce Solo, Local Solo and add it to Selenium2Library the browser cache.
        
        If the Robot Framework test code is executed through TeamCity using Sauce CI, the browser will be remotely instantiated throgh the Sauce service. Visit the documentation in the intro to see how the username and key are obtained
        See https://saucelabs.com/login
        
        Returns the index of this browser instance which can be used later to
        switch back to it. Index starts from 1 and is reset back to it when
        `Close All Browsers` keyword is used. See `Switch Browser` for
        example.

        Optional alias is an alias for the browser instance and it can be used
        for switching between browsers (just as index can be used). See `Switch
        Browser` for more details.

        Possible values for local instance `browser` are as follows:

        | firefox          | FireFox   |
        | ff               | FireFox   |
        | internetexplorer | Internet Explorer |
        | ie               | Internet Explorer |
        | googlechrome     | Google Chrome |
        | gc               | Google Chrome |
        | chrome           | Google Chrome |
        | opera            | Opera         |
        | phantomjs        | PhantomJS     |
        | htmlunit         | HTMLUnit      |
        | htmlunitwithjs   | HTMLUnit with Javascipt support |
        | android          | Android       |
        | iphone           | Iphone        |
        | safari           | Safari        |
        
        Note, that you will encounter strange behavior, if you open
        multiple Internet Explorer browser instances. That is also why
        `Switch Browser` only works with one IE browser at most.
        For more information see:
        http://selenium-grid.seleniumhq.org/faq.html#i_get_some_strange_errors_when_i_run_multiple_internet_explorer_instances_on_the_same_machine

        Optional 'ff_profile_dir' is the path to the firefox profile dir if you
        wish to overwrite the default.
        
        """
        
        print '(open_pyro_browser)'
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
            #OperatingSystem().set_environment_variable("ONDEMAND_PYRO", "1111")    
            #os.environ['ONDEMAND_PYRO'] = ondemand_string
                        
        self._seleniumlib.maximize_browser_window()
        self._seleniumlib.set_selenium_speed(selenium_speed) 
        
    def sencha_login(self, user_name, password, element_on_next_page):
        """
        Using the instantiated browser from `Open Browser`, the page traverses through the login page and waits for the targeted element on the following page.
        """
        print '(login_sencha)'
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

    def selenium_drag_and_drop(self, locator_type, ele_source, ele_dest):
        self._seleniumlib.drag_and_drop('%s=%s' % (locator_type,ele_source), '%s=%s' % (locator_type,ele_dest))

    def selenium_check(self, locator_type, element_locator):
        self._seleniumlib.select_checkbox('%s=%s' % (locator_type,element_locator))
  
    def selenium_uncheck(self, locator_type, element_locator):
        self._seleniumlib.unselect_checkbox('%s=%s' % (locator_type,element_locator))
       
    def selenium_wait_for_element_present(self, locator_type, element_locator):
        self._seleniumlib.wait_until_page_contains_element('%s=%s' % (locator_type,element_locator))
    
    def selenium_verify_text_from_element(self, locator_type, element_locator, text):
        self._seleniumlib.element_text_should_be('%s=%s' % (locator_type,element_locator), text)
    
    def selenium_reload(self):
        self._seleniumlib.reload_page()
        
    def selenium_type(self, locator_type, element_locator, text):
        self._seleniumlib.input_text('%s=%s' % (locator_type,element_locator), text)
    
    def selenium_clear(self, locator_type, element_locator):
        self._seleniumlib.input_text('%s=%s' % (locator_type,element_locator), '')
        
    def selenium_verify_attribute_from_element(self, locator_type, element_locator, element_class_locator, text):
        attr_value = self._seleniumlib.get_element_attribute('%s=%s@%s' % (locator_type, element_locator, element_class_locator))
        BuiltIn().should_contain(text, attr_value)
    
    def selenium_click(self, locator_type, element_locator, wait_before_click=5):
        BuiltIn().sleep(wait_before_click)
        self._seleniumlib.click_element('%s=%s' % (locator_type,element_locator))
	
    def selenium_click_text_from_combobox(self, locator_type, element_locator, text):
        self.selenium_wait_for_element_present(locator_type, element_locator)
        self.selenium_click(locator_type, element_locator)
        self.selenium_click('xpath', "//li[contains(@class, 'x-boundlist-item') and contains(text(),'%s')]" % text) 
    
    def selenium_populate_combo_and_click_text(self, locator_type, element_locator, text, wait_before_click=5):
        self.selenium_wait_for_element_present(locator_type, element_locator)
        self.selenium_click(locator_type, element_locator)
        self.selenium_click('xpath', "//div[contains(concat(' ', @class, ' '), 'x-trigger-index-0 x-form-trigger x-form-arrow-trigger x-form-trigger-first')]")
        BuiltIn().sleep(wait_before_click)
        self.selenium_click('xpath', "//li[contains(text(), '%s')]" % text)

    def selenium_double_click(self, locator_type, element_locator):
        self._seleniumlib.double_click_element('%s=%s' % (locator_type, element_locator))
    
    def selenium_element_should_not_be_visible(self, locator_type, element_locator):
        self._seleniumlib.element_should_not_be_visible('%s=%s' % (locator_type, element_locator))
        
    def selenium_click_by_script(self, element_locator):
        self._seleniumlib.execute_javascript("window.document.getElementById('%s').click();" % element_locator)
    