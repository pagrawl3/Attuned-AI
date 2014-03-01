import zerorpc
import json

class RPC(object):
    def dataProcessor(self, data):
    	print json.dumps(data, sort_keys=False, indent=4)
        return "%s" % data
    def connectUser(self, data):
    	print json.dumps(data, sort_keys=False, indent=4)
    	success_object = {'success'	: True,	'dataExists': False}
    	return json.dumps(success_object)

server = zerorpc.Server(RPC())
server.bind("tcp://0.0.0.0:4242")
server.run()