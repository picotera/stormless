# -*- coding: utf-8 -*-
import webapp2
import urllib
import requests
import requests_toolbelt.adapters.appengine
import base64

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()


counts = {}

class Spout(webapp2.RequestHandler):
  def get(self):
    self.response.headers["Content-Type"] = "text/plain"
    self.response.write(counts)


def call(topology, payload):
    url = 'http://localhost:8080/' + base64.b64encode(b'{}?{}'.format(topology, payload))
    response = requests.get(url)
    return response


class Bolt(webapp2.RequestHandler):
  topology = """{
\"spout\": (lambda x: (\"split\", \"how much wood would the woodchuck chuck if the wouldchuck could chuck wood\")),
\"split\": (lambda sentence: [(b\"count\",x) for x in sentence[0].split(\' \')] ),
\"count\": (lambda inputs: (counts.update({inputs[0]:counts.get(inputs[0], 0)+1}))),
}
"""

  def parse_payload(self, topology_str, topology, payload):
    if payload is None:
        call(topology_str, b"\"spout\"")
    elif isinstance(payload, basestring):
        if payload in topology:
            func_res = topology.get(payload)(None)
            self.parse_payload(topology_str, topology, func_res)
        else:
            self.response.write("error, no such func '%s'" % func_name)
    elif isinstance(payload, tuple):
        func_name, params = payload[0],payload[1:]
        if func_name in topology:
            func_res = topology.get(func_name)(params)
            call(topology_str, func_res)
        else:
            self.response.write("error, no such func '%s'" % func_name)
    elif isinstance(payload, list):
        for input_set in payload:
            call(topology_str, input_set)


  def get(self, data):
    self.response.headers["Content-Type"] = "text/plain"
    if not data:
        payload = None
        topology_str = self.topology
    else:
        decoded_data = base64.decodestring(data)
        split_data = decoded_data.split('?')
        topology_str = split_data[0]
        payload = eval(split_data[1])
        if payload is None:
            return



    if isinstance(topology_str, basestring):
        topology = eval(topology_str)
    elif isinstance(topology_str, dict):
        topology = topology_str
    else:
        self.response.write("Topology error: '%s'" % topology_str)
    
    self.parse_payload(topology_str, topology, payload)

    self.response.write("Job submitted")
        

app = webapp2.WSGIApplication([
  ("/print", Spout),
  ("/(.*)", Bolt),
], debug=True)
