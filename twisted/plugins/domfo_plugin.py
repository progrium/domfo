from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet
from twisted.web.server import Site

from domfo import RedirectResource


class Options(usage.Options):
    optParameters = [["port", "p", 80, "The port number to listen on."],
                        ["listen", "l", "0.0.0.0", "The interface to listen on."],
                        ["resolver", "r", "/etc/resolv.conf", "The resolver to use for DNS"]]


class DomfoMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "domfo"
    description = "Simple domain forwarder"
    options = Options

    def makeService(self, options):
        """
        Construct a TCPServer from a factory defined in myproject.
        """
        return internet.TCPServer(int(options["port"]), Site(RedirectResource(options['resolver'])), interface=options['listen'])

serviceMaker = DomfoMaker()
