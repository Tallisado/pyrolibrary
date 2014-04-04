import urllib2
import json
import base64

url = 'https://saucelabs.com/rest/%s/%s/%s'
#seleniumlib._current_browser().session_id

class Wrapper:
    def __init__(self, sel2lib, sauce_user, sauce_key, job):
        print '(Wrapper) user:%s key:%s job:%s session:%s' % (sauce_user, sauce_key, job, sel2lib._current_browser().session_id)
        self.__dict__['sel2lib'] = sel2lib
        self.username = sauce_user
        self.accessKey = sauce_key
        self.jobName = job

    def id(self):
        return self.sel2lib._current_browser().session_id

    def dump_session_id(self):
        print "\rSauceOnDemandSessionID=%s job-name=%s" % (self.id(), self.jobName)

    def update_sauce_rest(self, status, tags=[]):
        sauceRest = SauceRest(self.username, self.accessKey)
        if status == 'PASSED':
            sauceRest.update(self.id(), {'passed': True})
        else:
            sauceRest.update(self.id(), {'passed': False})
        sauceRest.update(self.id(), {'tags': tags})
        print 'updated ...'
        print tags
        print status
        
    def set_build_number(self, buildNumber):
        sauceRest = SauceRest(self.username, self.accessKey)
        sauceRest.update(self.id(), {'build': buildNumber})

    def set_tags(self, tags):
        sauceRest = SauceRest(self.username, self.accessKey)
        sauceRest.update(self.id(), {'tags': tags})

    def job_passed(self):
        sauceRest = SauceRest(self.username, self.accessKey)
        sauceRest.update(self.id(), {'passed': True})

    def job_failed(self):
        sauceRest = SauceRest(self.username, self.accessKey)
        sauceRest.update(self.id(), {'passed': False})

    def get_public_job_link(self):
        token = hmac.new(
            "{}:{}".format(self.username, self.accessKey),
            self.id(),
            hashlib.md5
        ).hexdigest()

        return "https://saucelabs.com/jobs/{}?auth={}".format(self.id(), token)

    def get_job_link(self):
        return "https://saucelabs.com/jobs/{}".format(self.id())


    # automatic delegation:
    def __getattr__(self, attr):
        return getattr(self.sel2lib, attr)

    def __setattr__(self, attr, value):
        return setattr(self.sel2lib, attr, value)

"""
This class provides several helper methods to invoke the Sauce REST API.
"""
class SauceRest:
    def __init__(self, user, key):
        self.user = user
        self.key = key

    def buildUrl(self, version, suffix):
        return url %(version, self.user, suffix)

    """
    Updates a Sauce Job with the data contained in the attributes dict
    """
    def update(self, id, attributes):
        url = self.buildUrl("v1", "jobs/" + id)
        data = json.dumps(attributes)
        return self.invokePut(url, self.user, self.key, data)

    """
    Retrieves the details for a Sauce job in JSON format
    """
    def get(self, id):
        url = self.buildUrl("v1", "jobs/" + id)
        return self.invokeGet(url, self.user, self.key)

    def invokePut(self, theurl, username, password, data):
        request = urllib2.Request(theurl, data, {'content-type': 'application/json'})
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        request.add_header("Authorization", "Basic %s" % base64string)
        request.get_method = lambda: 'PUT'
        htmlFile = urllib2.urlopen(request)
        return htmlFile.read()

    def invokeGet(self, theurl, username, password):
        request = urllib2.Request(theurl)
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        request.add_header("Authorization", "Basic %s" % base64string)
        htmlFile = urllib2.urlopen(request)
        return htmlFile.read()