#!/usr/bin/env python
import sys
from twisted.internet import reactor
from twisted.application import internet, service
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.python import log
from twisted.names import client
from optparse import OptionParser

class RedirectResource(Resource):
    isLeaf = True
    
    def __init__(self, resolver):
        self.resolver = resolver
    
    def render_GET(self, request):
        host = request.requestHeaders.getRawHeaders('Host', [None])[0]
        host = host.split(':')[0] # Drop the port
        self.resolver.lookupText(host) \
            .addCallback(lambda r: self.do_redirect(host, r[0], request)) \
            .addErrback(lambda e: self.do_error(host, e, request))
        return NOT_DONE_YET
    
    def do_redirect(self, host, answers, request):
        for x in answers:
            data = str(x.payload.data[0])
            if 'location=' in data:
                location = data.split('=')[1]
                request.redirect(location)
                print "%s -> %s" % (host, location)
        request.finish()
    
    def do_error(self, host, e, request):
        # Perhaps do something more useful here
        request.finish()

def main():
    parser = OptionParser()
    parser.add_option('--port', '-p',
                      help="Port number for Redirect HTTP server (default 8080)",
                      default=8080, type='int')
    parser.add_option('--listen', '-l',
                      help="Interface for Redirect HTTP server to listen on",
                      default='0.0.0.0', type='str')
    parser.add_option('--resolver', '-r', 
                      help="Set the DNS resolver",
                      default='/etc/resolv.conf', type='str')
    opts, args = parser.parse_args()

    log.startLogging(sys.stdout)
    resolver = client.Resolver(opts.resolver)
    reactor.listenTCP(opts.port, Site(RedirectResource(resolver)), interface=opts.listen)
    reactor.run()

if __name__ == '__main__':
    main()
