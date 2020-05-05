#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
import json
from xlrelease.HttpRequest import HttpRequest
import org.slf4j.Logger as Logger
import org.slf4j.LoggerFactory as LoggerFactory

class ITopClient(object):

    def __init__(self, httpConnection):
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded' }
        self.httpConnection = httpConnection
        self.url = '/webservices/rest.php?version=%s' % self.httpConnection['apiVersion']
        self.user = self.httpConnection['username']
        self.pwd = self.httpConnection['password']
        self.params = {'url': self.httpConnection['url'], 'proxyHost': self.httpConnection['proxyHost'], 'proxyPort': self.httpConnection['proxyPort'], 'proxyUsername': self.httpConnection['proxyUsername'], 'proxyPassword': self.httpConnection['proxyPassword']}
        self.logger = LoggerFactory.getLogger('com.xebialabs.itop-plugin')

    def _buildData(self, json_data):
        encoded_data = json.dumps(json_data)
        return "auth_user=%(user)s&auth_pwd=%(pwd)s&json_data=%(data)s" % {'user':self.user, 'pwd':self.pwd, 'data': encoded_data}

    def _postRequest(self, json_data):
        encoded_data = self._buildData(json_data)
        return HttpRequest(self.params).post(self.url, encoded_data, headers=self.headers)

    def testServer(self):
        json_data = {
            'operation':'list_operations'
        }
        response = self._postRequest(json_data)
        if response.response:
            resObj = json.loads(response.response)
            code = resObj['code']
            if code == 0:
                return True
            else:
                self.logger.error(resObj['message'])
                return False
        else:
            return False

    def queryIncidents(self, query):
        incidents = {}
        json_data = {
            'operation': 'core/get',
            'class' : 'Incident',
            'key' : query
        }
        response = self._postRequest(json_data)

        if response.response:
            resObj = json.loads(response.response)
            code = resObj['code']
            if code == 0:
                if resObj['objects']:
                    objets = resObj['objects']
                    for (x,y) in objets.items():
                        incidents[y['key']] = y['fields']['title']
            print resObj['message']

        return incidents

    def getIncidentDetails(self, id):
        incident = {}
        json_data = {
            'operation': 'core/get',
            'class' : 'Incident',
            'key' : id
        }
        response = self._postRequest(json_data)

        if response.response:
            resObj = json.loads(response.response)
            code = resObj['code']
            if code == 0:
                if resObj['objects']:
                    objets = resObj['objects']

                    for (x,y) in objets.items():
                        if y['fields']:
                            incident['key'] = y['key']
                            incident['class'] = y['class']
                            for (z,w) in y['fields'].items():
                                incident[z] = json.dumps(w)

            print resObj['message']

        return incident

    def queryUserRequests(self, query):
        userRequests = {}
        json_data = {
            'operation': 'core/get',
            'class' : 'UserRequest',
            'key' : query
        }
        response = self._postRequest(json_data)
        
        if response.response:
            resObj = json.loads(response.response)
            code = resObj['code']
            if code == 0:
                if resObj['objects']:
                    objets = resObj['objects']

                    for (x,y) in objets.items():
                        userRequests[y['key']] = y['fields']['title']
            print resObj['message']

        return userRequests

    def createUserRequest(self, title, description, org_id, caller_id, comment):
        key = 0
        json_data = {
            'operation': 'core/create',
            'class' : 'UserRequest',
            'comment' : comment,
            'fields' : {
                'org_id': org_id,
                'caller_id': caller_id,
                'title' : title,
                'description' : description
            }
        }
        response = self._postRequest(json_data)

        if response.response:
            resObj = json.loads(response.response)
            code = resObj['code']

            if code == 0:
                if resObj['objects']:
                    objets = resObj['objects']
                    for (x,y) in objets.items():
                        key = y['key']
            print resObj['message']

        return key

    def getUserRequestDetails(self, key):
        userRequest = {}
        json_data = {
            'operation': 'core/get',
            'class' : 'UserRequest',
            'key' : key
        }
        response = self._postRequest(json_data)

        if response.response:
            resObj = json.loads(response.response)
            code = resObj['code']
            if code == 0:
                if resObj['objects']:
                    objets = resObj['objects']
                    for (x,y) in objets.items():
                        if y['fields']:
                            userRequest['key'] = y['key']
                            userRequest['class'] = y['class']
                            for (z,w) in y['fields'].items():
                                userRequest[z] = json.dumps(w)

            print resObj['message']
        
        return userRequest

        