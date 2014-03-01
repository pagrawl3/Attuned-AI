import zerorpc

class RPC(object):
    def processLikes(self, data):
    	print data
        return "%s" % data

server = zerorpc.Server(RPC())
server.bind("tcp://0.0.0.0:4242")
server.run()