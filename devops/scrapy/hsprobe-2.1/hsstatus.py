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

import string
import time
from threading import RLock, Condition
from datetime import datetime

import log
import probespec
import util
from portrange import PortRange

logger = log.get_logger()

class PortProbe(object):

    def __init__(self):
        self.port = None
        self.protocol = None
        self.start = None
        self.end = None
        self.status = None
        self.proto_status = None

    def better_than(self, probe):
        result = True
        if probe:
            if probe.status == 'DONE':
                if self.status == 'DONE':
                    if probe.proto_status:
                        result = self.proto_status
                else:
                    result = False
        return result


class HSStatus(object):
    """
    Tracks probe-status data for a hidden service.
    """

    def __init__(self, hostname, *first_ports):

        # Base32 HS address (without '.onion')
        self._hostname = hostname.lower()

        # PortSpec object specifying ports and protocols to probe
        self._probe_spec = probespec.ProbeSpec()

        # Ports to probe first (in order)
        self._first_ports = first_ports

        # Port probes in current run
        self._port_probes = []

        # Port-indexed map of port probes
        self._probe_map = {}

        self._port_range_iter = None
        self._current_port_range = None

        self._mutex = RLock()
        self._cv = Condition(self._mutex)
        self._current_probe = None
        self._start_time = None
        self._timeout = None


    def acquire(self):
        self._mutex.acquire()


    def release(self):
        self._mutex.release()


    def _next_port_range(self):
        if not self._port_range_iter:
            port_ranges = []
            for port in self._first_ports:
                port_ranges.append(PortRange(port))
            port_ranges += self._probe_spec.port_ranges()
            self._port_range_iter = iter(port_ranges)
        try:
            self._current_port_range = self._port_range_iter.next()
        except StopIteration:
            self._current_port_range = None
        return self._current_port_range


    def _get_port_range(self):
        port_range = self._current_port_range
        if not port_range:
            port_range = self._next_port_range()
        return port_range


    def _next_specified_port(self):
        next_port = None
        port_range = self._get_port_range()
        while port_range:
            next_port = port_range.next()
            if next_port:
                break;
            port_range = self._next_port_range()
        return next_port


    def next_port(self):
        next_port = None
        self.acquire()
        try:
            next_port = self._next_specified_port()
            while next_port and self._probe_map.has_key(next_port):
                next_port = self._next_specified_port()
        finally:
            self.release()
        return next_port


    def protocols(self, port):
        self.acquire()
        try:
            protos = self._probe_spec.protocols(port)
        finally:
            self.release()
        return protos


    def set_probe_spec(self, probe_spec):
        self.acquire()
        try:
            self._probe_spec = probe_spec
        finally:
            self.release()


    def set_probe_start(self, ts, port, protocol):
        self.acquire()
        try:
            probe = PortProbe()
            probe.start = ts
            probe.port = port
            probe.protocol = protocol
            self._current_probe = probe
            self._probe_map[port] = probe
        finally:
            self.release()


    def set_timeout(self, timeout):
        self.acquire()
        try:
            self._start_time = time.time()
            self._timeout = float(timeout)
        finally:
            self.release()


    def time_remaining(self):
        remaining = None
        self.acquire()
        try:
            remaining = util.time_remaining(self._start_time, self._timeout)
            if remaining:
                logger.debug("Probe of %s will time out in %.2f seconds" % (self._hostname, remaining))
        finally:
            self.release()
        return remaining


    def wait(self, timeout=None):
        if timeout:
            start = datetime.now()
            self._cv.wait(timeout)
            end = datetime.now()
            td = end - start
            remaining = timeout - (td.seconds + td.microseconds/1000000.0)
            return max(remaining, 0.0)
        else:
            self._cv.wait()
            return None


    def wait_for_probe(self, timeout):
        probe = None
        self.acquire()
        try:
            probe = self._current_probe
            if probe:
                remaining = timeout
                while remaining > 0.0 and not probe.status:
                    remaining = self.wait(remaining)
                if not probe.status:
                    probe.end = time.time()
                    probe.status = 'STATUS_TIMEOUT'
                self._port_probes.append(probe)
                self._current_probe = None
        finally:
            self.release()
        if not probe:
            logger.warn("Status wait requested for %s when no probe active", self.hostname())
        return probe


    def notify(self, n=None):
        self._cv.notify(n)


    def notifyAll(self):
        self._cv.notifyAll()


    def _notify_status(self, ts, status, override=False):
        self.acquire()
        try:
            probe = self._current_probe
            if probe:
                if override or not probe.status:
                    probe.end = ts
                    probe.status = status
                    self.notifyAll()
        finally:
            self.release()
        if not probe:
            logger.debug("Received probe status %s for %s when no probe active (ignored)", str(status), self.hostname())


    def notify_status(self, ts, status):
        self._notify_status(ts, status)


    def override_status(self, ts, status):
        self._notify_status(ts, status, True)


    def set_proto_status(self, proto_status):
        self.acquire()
        try:
            probe = self._current_probe
            if probe:
                probe.proto_status = proto_status
                self.notifyAll()
        finally:
            self.release()


    # Immutable
    def hostname(self):
        self.acquire()
        try:
            hostname = self._hostname
        finally:
            self.release()
        return hostname


    def first_ports(self):
        self.acquire()
        try:
            first_ports = self._first_ports
        finally:
            self.release()
        return first_ports


    def port_probes(self):
        self.acquire()
        try:
            port_probes = self._port_probes
        finally:
            self.release()
        return port_probes


    def best_probe(self):
        self.acquire()
        try:
            best_probe = None
            for probe in self._port_probes:
                if probe.better_than(best_probe):
                    best_probe = probe
        finally:
            self.release()
        return best_probe


    def last_probe(self):
        self.acquire()
        try:
            port_probes = self._port_probes
            last_probe = port_probes[-1] if len(port_probes) > 0 else None
        finally:
            self.release()
        return last_probe


    def to_csv(self):
        lst = []
        self.acquire()
        try:
            lst.append(self._output_val(self.hostname()))
            best_probe = self.best_probe()
            port = best_probe.port if best_probe else None
            start = int(best_probe.start) if best_probe else None
            status = best_probe.status if best_probe else None
            protocol = best_probe.protocol if best_probe and best_probe.proto_status else None
            lst.append(self._output_val(port))
            lst.append(self._output_val(start))
            lst.append(self._output_val(status))
            lst.append(self._output_val(protocol))
        finally:
            self.release()
        return string.join(lst, ',')


    def _output_val(self, value):
        return str(value) if value else ""


def from_fields(fields):
    hostname = _field_value(fields, 0)
    if not hostname:
        raise SyntaxError("HS must have a hostname")
    first_ports = []
    for field in fields[1:]:
        try:
            port = int(field)
            if port > 0 and port < 65536:
                first_ports.append(port)
            else:
                break
        except:
            break

    return HSStatus(hostname, *first_ports)


def _field_value(fields, i):
    value = None
    if len(fields) > i:
        if fields[i] != "":
            value = fields[i]
    return value
