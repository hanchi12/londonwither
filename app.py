#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    
    baseurl = "http://samples.openweathermap.org/data/2.5/weather?zip=01485,ph&appid=66910cc54f55f6bc8de8dc666ccb3120"
    
    result = urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def makeWebhookResult(data):
    
    query = data.get('coord')
    
    # print(json.dumps(item, indent=4))

    speech = "Request Message "+ "xxx" + " ..."
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
