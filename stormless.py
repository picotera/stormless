# -*- coding: utf-8 -*-
import webapp2
import urllib
import requests
import requests_toolbelt.adapters.appengine
import base64

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

stormless_delimiter = "???"

data = {}

class Data(webapp2.RequestHandler):
  def get(self):
    self.response.headers["Content-Type"] = "text/plain"
    self.response.write(data)


def call(payload, topology, utils):
    url = 'http://localhost:8080/' + base64.b64encode(b'{payload}{d}{topology}{d}{utils}'.format(d=stormless_delimiter,
        payload=payload, 
        topology=topology, 
        utils=utils))
    response = requests.get(url)
    return response


class Bolt(webapp2.RequestHandler):
  topology = """{
\"spout\": (lambda x: (\"split\", \"how much wood would the woodchuck chuck if the woodchuck could chuck wood\")),
\"split\": (lambda sentence: [(\"count\",x) for x in sentence[0].split(\' \')] ),
\"count\": (lambda inputs: (data.update({inputs[0]:data.get(inputs[0], 0)+1}))),
}
"""

  def parse_payload(self, topology_str, topology, payload, utils_str):
    if payload is None:
        call(b"\"spout\"", topology_str, utils_str)
    elif isinstance(payload, basestring):
        if payload in topology:
            func_res = topology.get(payload)(None)
            self.parse_payload(topology_str, topology, func_res, utils_str)
        else:
            error = "error, no such func '%s'" % func_name
            data["STORMLESS_INTERNAL_ERROR"] = error
            self.response.write(error)
    elif isinstance(payload, tuple):
        func_name, params = payload[0],payload[1:]
        if func_name in topology:
            func_res = topology.get(func_name)(params)
            call(func_res, topology_str, utils_str)
        else:
            error = "error, no such func '%s'" % func_name
            data["STORMLESS_INTERNAL_ERROR"] = error
            self.response.write(error)
    elif isinstance(payload, list):
        for sub_res in payload:
            call(sub_res, topology_str, utils_str)


  def get(self, data):
    self.response.headers["Content-Type"] = "text/plain"
    utils_str = None
    payload = None
    topology_str = self.topology
    if data:
        decoded_data = base64.decodestring(data)
        split_data = decoded_data.split(stormless_delimiter)
        payload = eval(split_data[0])
        if payload is None:
            return
        topology_str = split_data[1]
        if len(split_data) > 2:
            utils_str = split_data[2]
            exec(utils_str)

    if isinstance(topology_str, basestring):
        topology = eval(topology_str)
    elif isinstance(topology_str, dict):
        topology = topology_str
    else:
        error = "Topology error: '%s'" % topology_str)
        data["STORMLESS_INTERNAL_ERROR"] = error
        self.response.write(error)

    self.response.write("Job submitted")

    self.parse_payload(topology_str, topology, payload, utils_str)
        

app = webapp2.WSGIApplication([
  ("/data", Data),
  ("/(.*)", Bolt),
], debug=True)
