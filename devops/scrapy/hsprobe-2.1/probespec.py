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

import log
from portrange import PortRange
from util import is_valid_port


logger = log.get_logger()


class _PortSpec(object):

    def __init__(self, low, high, protos=[]):
        self.low = low
        self.high = high
        self.protos = protos


    def has_port(self, port):
        return port >= self.low and port <= self.high


class ProbeSpec(object):

    def __init__(self):
        self._port_specs = []


    def port_ranges(self):
        port_ranges = []
        for port_spec in self._port_specs:
            port_ranges.append(PortRange(port_spec.low, port_spec.high))
        return port_ranges


    def protocols(self, port):
        proto_list = []
        proto_set = set(proto_list)
        for port_spec in self._port_specs:
            if port_spec.has_port(port):
                for proto in port_spec.protos:
                    if proto not in proto_set:
                        proto_list.append(proto)
                        proto_set.add(proto)
        return proto_list if len(proto_list) > 0 else ['none']


def from_string(line, probe_spec=ProbeSpec(), where=""):
    line = line.strip()
    fields = line.split('#', 2)
    content = fields[0]
    if len(content) <= 0:
        return probe_spec

    fields = content.split(':', 2)
    portstr = fields[0]
    protostr = fields[1] if len(fields) > 1 else ''

    port_specs = []
    for port_range in portstr.split(','):
        port_range = port_range.strip()
        ports = port_range.split('-', 2)
        low = ports[0].strip()
        high = ports[1].strip() if len(ports) > 1 else low
        valid = False
        if is_valid_port(low) and is_valid_port(high):
            low_port = int(low)
            high_port = int(high)
            if low_port <= high_port:
                valid = True
                port_specs.append(_PortSpec(low_port, high_port))
        if not valid:
            logger.warn("Invalid port range '%s'%s (ignored)" % (port_range, where))
            continue

    proto_list = []
    for proto in protostr.split(','):
        proto = proto.strip()
        if len(proto) > 0:
            proto_list.append(proto.lower())

    for port_spec in port_specs:
        port_spec.protos = proto_list

    probe_spec._port_specs += port_specs
    return probe_spec


def from_file(path, probe_spec=ProbeSpec()):
    try:
        fp = open(path, 'r')
    except Exception as err:
        logger.error("Failed to open %s: %s" % (path, err))
        return None

    lineno = 0
    for line in fp:
        lineno += 1
        where = " at %s line %d" % (path, lineno)
        probe_spec = from_string(line, probe_spec, where)

    return probe_spec


def from_list(lines, probe_spec=ProbeSpec()):
    for line in lines:
        probe_spec = from_string(line, probe_spec)
    return probe_spec
