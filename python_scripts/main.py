import zerorpc
import json

class RPC(object):
    def processLikes(self, data):
    	print json.dumps(data, sort_keys=False, indent=4)
        return "%s" % data

server = zerorpc.Server(RPC())
server.bind("tcp://0.0.0.0:4242")
server.run()