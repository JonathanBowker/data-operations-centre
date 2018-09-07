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

import threading
from threading import Thread, Lock, RLock, Condition
from Queue import Queue, Empty
import time
from datetime import datetime
import urllib2
from urllib2 import HTTPError
import httplib
import socks
import sys
import select
import zlib

from stem import StreamStatus
from stem.control import EventType

import hsstatus
import proxyurl
import log
import util


logger = log.get_logger()

hs_sfx = ".onion"
hs_sfx_len = len(hs_sfx)

def thread_name():
    return threading.currentThread().getName()


class ProbeManager(object):

    def __init__(self, controller, probe_spec, args):
        self._controller = controller
        self._probe_spec = probe_spec
        self._args = args
        self._mutex = Lock()
        self._hs_queue = Queue(args.queue_size)
        self._max_threads = args.num_threads
        self._thread_tracker = _ThreadTracker()
        self._output_mutex = Lock()
        self._start_time = None
        self._end_time = None
        self._probe_count = 0
        self._probe_map = {}
        self._probe_map_mutex = Lock()
        self._next_action = {
            'MISC'           : self._retry_next,
            'RESOLVEFAILED'  : self._fail,
            'CONNECTREFUSED' : self._try_next_port,
            'EXITPOLICY'     : self._try_next_port,
            'DESTROY'        : self._retry_once,
            'DONE'           : self._pass,
            'TIMEOUT'        : self._retry_once,
            'NOROUTE'        : self._fail,
            'HIBERNATING'    : self._fail,
            'INTERNAL'       : self._retry_once,
            'RESOURCELIMIT'  : self._retry_once,
            'CONNRESET'      : self._retry_next,
            'TORPROTOCOL'    : self._retry_once,
            'NOTDIRECTORY'   : self._retry_once,
            'CANT_ATTACH'    : self._retry_once,
            }
        self._default_next_action = self._fail

        _proxy_args = (socks.PROXY_TYPE_SOCKS5, "127.0.0.1", self._args.socks_port, True)
        socks.setdefaultproxy(*_proxy_args)
        self._proxy_url = proxyurl.ProxyURLHandler(*_proxy_args)


    def lock(self):
        self._mutex.acquire()


    def unlock(self):
        self._mutex.release()


    def start(self):
        started = False
        self.lock()
        try:
            if self._start_time:
                started = True
            else:
                self._start_time = time.time()
        finally:
            self.unlock()
        if started:
            return

        logger.debug("Probe manager started")

        self._controller.add_event_listener(self._stream_event, EventType.STREAM)

        self._probe_all()

        self._thread_tracker.waitForThreads()
        logger.debug("Thread tracker done")

        self._args.output.flush()
        logger.debug("Probe manager done")


    def threads_active(self):
        return self._thread_tracker.threads_active()


    def threads_started(self):
        return self._thread_tracker.threads_started()


    def output(self, line):
        self._output_mutex.acquire()
        try:
            print >>self._args.output, line
        finally:
            self._output_mutex.release()


    def probe(self, hs_status):
        hs_status.set_timeout(self._args.probe_timeout)
        probe = self._try_next_port(hs_status)
        while probe:
            next_action = self._default_next_action
            if self._next_action.has_key(probe.status):
                next_action = self._next_action[probe.status]
#            logger.debug("Next action for %s is %s" % (probe.status, str(next_action)))
            probe = apply(next_action, (hs_status, probe))

        self._finish(hs_status)

        return


    def _probe_port(self, hs_status, port):
        for protocol in hs_status.protocols(port):
            probe = self._probe_protocol(hs_status, port, protocol)
            if not probe or probe.status != 'DONE':
                break
        return probe
        

    def _probe_protocol(self, hs_status, port, protocol):
        hostname = hs_status.hostname()
        address = hostname + hs_sfx
        start_ts = time.time()
        hs_status.set_probe_start(start_ts, port, protocol)
        self.record_probe(hostname, hs_status)

        logger.info("Probing protocol '%s' on %s:%d" % (protocol, address, port))

        method_name = "_probe_proto_" + protocol
        try:
            method = getattr(self, method_name)
            result = method(address, port, hs_status.time_remaining())
            hs_status.set_proto_status(result)
            if result:
                # If the protocol test succeeded, call the probe successful,
                # regardless of the status returned by Tor.
                hs_status.override_status(time.time(), 'DONE')
        except AttributeError:
            hs_status.override_status(time.time(), 'PROBE_ERROR')
            logger.error("No method to probe protocol '%s'" % protocol)

        # Wait for the connection status result from Tor
        # (done by _stream_event, running in the Stem event-notifier thread)
        probe = hs_status.wait_for_probe(hs_status.time_remaining())
        if probe:
            logger.debug("Probe of '%s' on %s:%d returned status %s" % (protocol, address, port, probe.status))
        else:
            logger.error("Probe of '%s' on %s:%d failed" % (protocol, address, port))

        self.delete_probe(hostname)

        return probe


    def _fail(self, hs_status, last_probe=None):
        logger.debug("No further action on %s" % hs_status.hostname())
        return None


    def _finish(self, hs_status, last_probe=None):
        self.output(hs_status.to_csv())


    def _try_next_port(self, hs_status, last_probe=None):
        probe = None
        port = hs_status.next_port()
        if port:
            logger.debug("Next port for %s is %d" % (hs_status.hostname(), port))
            probe = self._probe_port(hs_status, port)
        else:
            logger.debug("No more ports for %s" % hs_status.hostname())
        return probe


    def _pass(self, hs_status, last_probe):
        logger.debug("Probe successful for %s on port %d" % (hs_status.hostname(), last_probe.port))
        return None


    def _retry_once(self, hs_status, last_probe):
        port = last_probe.port
        logger.debug("Retrying %s on port %d" % (hs_status.hostname(), port))
        probe = self._probe_port(hs_status, port)
        return probe if probe.status != last_probe.status else None


    def _retry_next(self, hs_status, last_probe):
        probe = self._retry_once(hs_status, last_probe)
        if not probe:
            # Result was the same; try other ports
            return self._try_next_port(hs_status)
        else:
            # Result changed; handle according to new result
            return probe


    def _probe_all(self):
        lineno = 0
        for line in self._args.input:
            lineno += 1
            record = line.rstrip()
            if record.startswith('#'):
                self.output(record)
                continue
            fields = record.split(',')
            try:
                hs_status = hsstatus.from_fields(fields)
                hs_status.set_probe_spec(self._probe_spec)
                self._check_start_threads()
                self._hs_queue.put(hs_status)
            except SyntaxError as err:
                logger.warn("Failed to parse hidden service data at %s line %d: %s"
                            % (self._args.input_file, lineno, str(err)))


    def _check_start_threads(self):
        while self._need_more_threads():
            self._thread_tracker.runDaemonThread(self._start_probe)


    def _need_more_threads(self):
        result = None
        num_active = self.threads_active()
        if num_active < 1:
            result = True
        elif num_active >= self._max_threads:
            result = False
        elif self._hs_queue.qsize() > 2 * num_active:
            result = True
        else:
            result = False
        return result


    def _keep_this_thread(self):
        #return self._hs_queue.qsize() >= self.threads_active()
        return self._hs_queue.qsize() > 0


    def _start_probe(self):
        running = True
        while running:
            try:
                hs_status = self._hs_queue.get(True, 5)
                self.probe(hs_status)
                if not self._keep_this_thread():
                    running = False
            except Empty:
                running = False
            except Exception as err:
                logger.error("Probe failed with exception: %s", str(err))


    def find_probe(self, key):
        return self._find_probe(key, False)


    def delete_probe(self, key):
        return self._find_probe(key, True)


    def record_probe(self, key, value):
        result = None
        self._probe_map_mutex.acquire()
        try:
            self._probe_map[key] = value
        finally:
            self._probe_map_mutex.release()
        return value


    def _find_probe(self, key, delete=False):
        result = None
        self._probe_map_mutex.acquire()
        try:
            if self._probe_map.has_key(key):
                result = self._probe_map[key]
                if delete:
                    del(self._probe_map[key])
        finally:
            self._probe_map_mutex.release()
        return result


    def _stream_event(self, event):
        ts = time.time()
        if event.status == StreamStatus.CLOSED:
            addr = event.target_address
            if addr.endswith(hs_sfx):
                # StreamClosureReason always handled as strings, since Tor sometimes
                # returns values not present in the StreamClosureReason enum.
                reason = str(event.reason)
                remote_reason = str(event.remote_reason)
                logger.debug("target=%s, target_address=%s, target_port=%d, reason=%s, remote_reason=%s"
                             % (event.target, event.target_address, event.target_port,
                                reason, remote_reason))
                hostname = addr[0:-hs_sfx_len]
                hs_status = self.find_probe(hostname)
                if hs_status:
                    status = reason
                    if status == 'END':
                        status = remote_reason
                    hs_status.notify_status(ts, status)
                else:
                    logger.debug("Received status event for %s with no probe active (ignored)", hostname)


    def _probe_proto_none(self, address, port, timeout=None):
        try:
            s = socks.socksocket()
            s.settimeout(timeout)
            s.connect((address, port))
            s.close()
            return True
        except Exception as err:
            logger.debug("Connect to %s:%d failed: %s" % (address, port, err))
        return None


    def _probe_proto_http(self, address, port, timeout=None):
        return self.__proto_http("http", address, port, timeout)


    def _probe_proto_https(self, address, port, timeout=None):
        return self.__proto_http("https", address, port, timeout)


    _http_headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding' : 'gzip, deflate',
        'Connection' : 'keep-alive',
        }

    def __proto_http(self, scheme, address, port, timeout=None):
        url = scheme + "://" + address + ":" + str(port) + "/"
        request = urllib2.Request(url=url, headers=self._http_headers)
        result = None
        response = None
        t1 = time.time()

        try:
            # response is a urllib.addinfourl object
            response = self._proxy_url.open_url(request, timeout=timeout)
        except HTTPError as http_err:
            # HTTPError implies a response from an HTTP server
            # (but indicating something other than success), and
            # since it is also a urllib.addinfourl object, it can be
            # handled just like a normal response.
            response = http_err
        except Exception as err:
            logger.debug("%s failed: %s" % (url, err))

        if response:
            try:
                status_code = response.getcode()
                logger.debug("%s returned HTTP status code %s" % (url, status_code))
                result = True
                remaining = util.time_remaining(t1, timeout)
                self._process_response(response, scheme, address, port, remaining, self._args.download_limit)
            finally:
                response.close()
        return result


    def _process_response(self, infile, proto, address, port, timeout=None, dl_limit=sys.maxint):
        download_dir = self._args.download_dir
        try:
            util.mkdir_p(download_dir)
        except Exception as e:
            logger.error("Failed to create download directory %s: %s" %s (download_dir, err))
            return None

        host = address[0:-hs_sfx_len] if address.endswith(hs_sfx) else address
        outfilename = "%s/%s_%s_%s" % (download_dir, host, port, proto)
        try:
            outfile = open(outfilename, 'w')
        except Exception as err:
            logger.error("Failed to open %s for output: %s" % (outfilename, err))
            return None

        try:
            http_code = infile.getcode()
            headers = infile.info()
        except:
            http_code = 0
            headers = {}

        if http_code > 0:
            http_code_name = 'Unknown'
            if httplib.responses.has_key(http_code):
                http_code_name = httplib.responses[http_code]
            outfile.write("%d %s\n" % (http_code, http_code_name))
            for key in headers.keys():
                outfile.write("%s: %s\n" % (key, headers[key]))
            outfile.write("\n")

        decompressor = None
        if headers.has_key('content-encoding'):
            encoding = headers['content-encoding'].lower()
            if encoding in ['gzip', 'deflate', 'zlib']:
                decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)

        max_read = min(1024, dl_limit)
        total_len = 0
        remaining = timeout
        rin = [infile]
        win = []
        xin = []
        try:
            try:
                while total_len < dl_limit:
                    # Workaround for closed socket
                    try:
                        infile.fileno()
                    except:
                        break
                    t1 = time.time()
                    rout, wout, xout = select.select(rin, win, xin, remaining)
                    if infile not in rout:
                        logger.warn("Read timeout on %s:%d (proto %s)" % (address, port, proto))
                        break
                    data = infile.read(max_read)
                    data_len = len(data)
                    if data_len <= 0:
                        break
                    if decompressor:
                        ddata = decompressor.decompress(data)
                        outfile.write(ddata)
                        total_len += len(ddata)
                    else:
                        outfile.write(data)
                        total_len += data_len
                    remaining = util.time_remaining(t1, remaining)
            finally:
                outfile.close()
        except Exception as err:
            logger.error("Error while downloading to %s: %s" % (outfilename, err))
            return None

        return total_len


class _ThreadTracker(object):
    def __init__(self):
        self._mutex = RLock()
        self._cv = Condition(self._mutex)
        self._threads_started = 0
        self._threads_active = 0


    def acquire(self):
        self._mutex.acquire()


    def release(self):
        self._mutex.release()


    def wait(self, timeout=None):
        self._cv.wait(timeout)


    def notify(self, n=None):
        self._cv.notify(n)


    def notifyAll(self):
        self._cv.notifyAll()


    def threads_started(self):
        self.acquire()
        try:
            result = self._threads_started
        finally:
            self.release()
        return result


    def threads_active(self):
        self.acquire()
        try:
            result = self._threads_active
        finally:
            self.release()
        return result


    def runDaemonThread(self, target, *args):
        target_args = (target,) + args
        new_thread = Thread(target=self._runTarget, args=target_args)
        new_thread.setDaemon(True)
        new_thread.start()
        self.acquire()
        try:
            self._threads_started += 1
            self.notifyAll()
        finally:
            self.release()
        return new_thread


    def _runTarget(self, target, *args):
        self.acquire()
        try:
            self._threads_active += 1
            logger.debug("%s started; now %d active threads" % (thread_name(), self._threads_active))
            self.notifyAll()
        finally:
            self.release()
        apply(target, *args)
        self.acquire()
        try:
            self._threads_active -= 1
            logger.debug("%s terminated; now %d active threads" % (thread_name(), self._threads_active))
            self.notifyAll()
        finally:
            self.release()


    def waitForThreads(self, timeout=None):
        if self._threads_started > 0:
            remaining = timeout
            logger.debug("Waiting for probe threads to complete")
            self.acquire()
            try:
                while self._threads_active > 0:
                    if timeout:
                        start = datetime.now()
                        self.wait(remaining)
                        end = datetime.now()
                        td = end - start
                        remaining -= (td.seconds + td.microseconds/1000000.0)
                        if remaining <= 0:
                            break
                    else:
                        self.wait()
            finally:
                self.release()
            logger.debug("Probe threads have completed")
