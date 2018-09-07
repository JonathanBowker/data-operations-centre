"""
Copyright (c) 2014, SRI International
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

* Neither the name of SRI International nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import socket
import urllib2
import httplib
import ssl

import socks
import log


logger = log.get_logger()

class ProxyURLHandler(object):

    def __init__(self, *args, **kwargs):
        self.opener = urllib2.build_opener(
            SocksHTTPHandler(*args, **kwargs),
            SocksHTTPSHandler(*args, **kwargs)
            )

    def open_url(self, url, data=None, timeout=None):
        return self.opener.open(url, data, timeout)


class SocksHTTPHandler(urllib2.HTTPHandler):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        urllib2.HTTPHandler.__init__(self)

    def http_open(self, req):
        def conn_factory(host, port=None, strict=None, timeout=None):
            conn = SocksHTTPConnection(*self.args, host=host, port=port, strict=strict, timeout=timeout, **self.kwargs)
            return conn
        return self.do_open(conn_factory, req) # urllib2.AbstractHTTPHandler


class SocksHTTPConnection(httplib.HTTPConnection):

    def __init__(self, ptype=None, paddr=None, pport=None, rdns=True, puser=None, ppass=None, *args, **kwargs):
        self.proxy_args = (ptype, paddr, pport, rdns, puser, ppass)
        httplib.HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(*self.proxy_args)
        if type(self.timeout) in (int, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))


class SocksHTTPSHandler(urllib2.HTTPSHandler):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        urllib2.HTTPSHandler.__init__(self)

    def https_open(self, req):
        def conn_factory(host, port=None, strict=None, timeout=None):
            conn = SocksHTTPSConnection(*self.args, host=host, port=port, strict=strict, timeout=timeout, **self.kwargs)
            return conn
        return self.do_open(conn_factory, req) # urllib2.AbstractHTTPHandler


class SocksHTTPSConnection(httplib.HTTPSConnection):

    def __init__(self, ptype=None, paddr=None, pport=None, rdns=True, puser=None, ppass=None, *args, **kwargs):
        self.proxy_args = (ptype, paddr, pport, rdns, puser, ppass)
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(*self.proxy_args)
        if type(self.timeout) in (int, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
        self.sock = ssl.wrap_socket(self.sock, self.key_file, self.cert_file)
