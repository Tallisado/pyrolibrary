import urllib2
import json
import base64

url = 'https://saucelabs.com/rest/%s/%s/%s'

class SauceRestWrapper:
    def __init__(self):
        pass
        
    def establish(self, job_id, sauce_user, sauce_key, job_name):
        print '(Wrapper) user:%s key:%s job:%s session:%s' % (sauce_user, sauce_key, job_name, job_id)
        self.__dict__['sel2lib'] = sel2lib
        self.job_id = job_id
        self.username = sauce_user
        self.access_key = sauce_key
        self.job_name = job_name

    def id(self):
        return self.job_id

    def dump_session_id(self):
        print "\rSauceOnDemandSessionID=%s job-name=%s" % (self.id(), self.job_name)

    def update_sauce_rest(self, status, tags=[]):
        sauceRest = SauceRest(self.username, self.access_key)
        if status == 'PASSED':
            sauceRest.update(self.id(), {'passed': True})
        else:
            sauceRest.update(self.id(), {'passed': False})
        sauceRest.update(self.id(), {'tags': tags})
        print 'updated ...'
        print tags
        print status
        
    def set_build_number(self, buildNumber):
        sauceRest = SauceRest(self.username, self.access_key)
        sauceRest.update(self.id(), {'build': buildNumber})

    def set_tags(self, tags):
        sauceRest = SauceRest(self.username, self.access_key)
        sauceRest.update(self.id(), {'tags': tags})

    def job_passed(self):
        sauceRest = SauceRest(self.username, self.access_key)
        sauceRest.update(self.id(), {'passed': True})

    def job_failed(self):
        sauceRest = SauceRest(self.username, self.access_key)
        sauceRest.update(self.id(), {'passed': False})

    def get_public_job_link(self):
        token = hmac.new(
            "{}:{}".format(self.username, self.access_key),
            self.id(),
            hashlib.md5
        ).hexdigest()

        return "https://saucelabs.com/jobs/{}?auth={}".format(self.id(), token)

    def get_job_link(self):
        return "https://saucelabs.com/jobs/{}".format(self.id())

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