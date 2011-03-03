#!/usr/bin/env python
try:
    from twisted.internet import pollreactor 
    pollreactor.install()
except: pass
from twisted.internet import reactor
from twisted.application import internet, service
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.python import log
from twisted.names import client
import sys, os, string

def opt(name, default=None, cast=str): return cast(os.environ.get(name, default))

class RedirectResource(Resource):
    isLeaf = True
    
    def __init__(self, resolver):
        self.resolver = client.Resolver(resolver)
    
    def render_GET(self, request):
        host = request.requestHeaders.getRawHeaders('Host', [None])[0]
        host = 'redirect.' + host.split(':')[0] # Drop the port
        print "Looking up (new method): %s" % host
        self.resolver.lookupText(host) \
            .addCallback(lambda r: self.do_redirect(host, r[0], request)) \
            .addErrback(lambda e: self.backwards_compat(request))
        return NOT_DONE_YET

    def backwards_compat(self, request):
        host = request.requestHeaders.getRawHeaders('Host', [None])[0]
        host = host.split(':')[0] # Drop the port
        print "Looking up (old method): %s" % host
        self.resolver.lookupText(host) \
            .addCallback(lambda r: self.do_redirect(host, r[0], request)) \
            .addErrback(lambda e: self.do_error(host, e, request))
        return NOT_DONE_YET

    def do_redirect(self, host, answers, request):
        for x in answers:
            data = str(x.payload.data[0])
            if data.startswith('location='):
                location = data.split('=')[1]
                location = location[0:-1] if location[-1] == '/' else location
                if string.count(location,"/") == 2:
                  location = location + request.path
                request.redirect(location)
                print "%s -> %s" % (host, location)
        request.finish()
    
    def do_error(self, host, e, request):
        # Perhaps do something more useful here
        request.finish()

    
port        = opt('PORT', 8080, int)
interface   = opt('INTERFACE', '0.0.0.0', str)
resolver    = opt('RESOLVER', '/etc/resolv.conf', str)
factory     = Site(RedirectResource(resolver))

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    reactor.listenTCP(port, factory, interface=interface)
    reactor.run()
else:
    application = service.Application('domfo')
    internet.TCPServer(port, factory, interface=interface).setServiceParent(application)
