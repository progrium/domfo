# domfo
Simple DNS-configured domain forwarding service

This is a simple web server that redirects requests to the location found in the TXT record for the redirect subdomain in the host of the incoming request. There is no security, it's intended for public use.

If you want to use it to redirect your new domain "www.domain.com" to "http://www.otherdomain.com", you set up two DNS records for domain.com:

 * www.domain.com CNAME "domfo.progrium.com" (You may need to use an A record for SLD names)
 * redirect.www.domain.com TXT "location=http://www.otherdomain.com"
 
And you're done! Requests to http://www.domain.com will redirect to http://www.otherdomain.com once DNS propagates. 