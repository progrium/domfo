import string
import gevent.pywsgi

import dns.resolver

from gservice.config import Option
from gservice.core import Service

class DomainForwarder(Service):
    bind_address = Option('bind_address')
    
    def __init__(self):
        self.server = gevent.pywsgi.WSGIServer(self.bind_address, self.handle)
        self.add_service(self.server)
    
    def handle(self, environ, start_response):
        host = environ.get('HTTP_HOST')
        host = 'redirect.' + host.split(':')[0] # Drop the port
        answers = dns.resolver.query(host, 'TXT')
        location = None
        try:
            for answer in answers:
                for data in answer.strings:
                    if data.startswith('location='):
                        location = data.split('=')[1]
                        location = location[0:-1] if location[-1] == '/' else location
                        if string.count(location,"/") == 2:
                            location = "%s%s" % (location, environ.get('PATH_INFO'))
                        break
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass
        if location:
            print "%s -> %s" % (host, location)
            start_response("301 Redirect", {"Location": location})
            return "Redirecting..."
        else:
            start_response("404 Not Found", [])
            return "No location found to forward to."