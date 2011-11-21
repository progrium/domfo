domfo
=====

Domain Forwarder

This is a simple web server that redirects requests to the location found in the TXT record for the domain in the host of the incoming request. There is no security, so if somebody knows the host/IP of your running domfo instance, they can use it to forward their domain.

Here's how you use it once it's running. Say it's running on port 80 at redirect.domdori.com ... so if you want to use it to redirect your new domain "superdomain.com" to "http://myblog.com", you set up two DNS records for superdomain.com:

 * CNAME record to redirect.domdori.com
 * TXT record with "location=http://myblog.com"
 
And you're done! Requests to http://superdomain.com will redirect to http://myblog.com once DNS propagates. 