#!/usr/bin/env python

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

import logging
import os
import time
import string
import argparse
from argparse import RawDescriptionHelpFormatter
import re
import commands
import sys

import stem
import stem.connection
import stem.process
from stem.control import Controller

import log
from probemgr import ProbeManager
import probespec
import util

version = "2.1"

logger = log.get_logger()


def main():
    """
    Main
    """

    args = parse_args()

    logger.setLevel(logging.__dict__[string.upper(args.verbosity)])

    logger.info("Version %s" % version)
    logger.info("Command line arguments: %s" % str(args))

    if args.sentinel_file:
        try:
            os.remove(args.sentinel_file)
        except:
            pass

    if args.spec_file:
        probe_spec = probespec.from_file(args.spec_file)
    elif args.probe_spec:
        probe_spec = probespec.from_list(args.probe_spec)
        
    if not probe_spec:
        logger.error("No probe specification; terminating")
        sys.exit(1)

    if args.input_file:
        args.input = open(args.input_file, 'r')
    else:
        args.input_file = "<stdin>"
        args.input = sys.stdin

    if args.output_file:
        args.output = open(args.output_file, 'w')
    else:
        args.output_file = "<stdout>"
        args.output = sys.stdout

    if args.clear_tor_data_dir:
        logger.debug("Clearing Tor data dir %s; output below:" % args.tor_data_dir)
        logger.debug(commands.getoutput("rm -f %s/*" % args.tor_data_dir))

    launch_tor(args)
    controller = Controller.from_port(port=args.control_port)
    stem.connection.authenticate(controller)

    logger.debug("Redirecting Tor log (level %s) to %s" % (args.tor_log_level, args.tor_log_file))
    controller.set_conf("Log", "%s file %s" % (args.tor_log_level, args.tor_log_file))

    probemgr = ProbeManager(controller, probe_spec, args)
    probemgr.start()

    logger.debug("Closing controller connection")
    controller.close()

    if args.sentinel_file:
        sf = open(args.sentinel_file, 'w')
        sf.close()

    return 0


def parse_args():
    """
    Parses command line arguments.
    """

    desc =  "%s, version %s\n" % (os.path.basename(__file__), version)
    desc += "Copyright (c) 2014, SRI International\nAll rights reserved\n"
    desc += "This software is provided with NO WARRANTY.  See LICENSE for details.\n"
    desc += "\nProbes Tor hidden services."
    parser = argparse.ArgumentParser(description=desc, formatter_class=RawDescriptionHelpFormatter)

    group = parser.add_mutually_exclusive_group()

    default_spec_file = "%s/%s" % (util.script_dir(), "probe_spec")
    group.add_argument("-b", "--spec-file", type=str,
                       help="File specifying ports and protocols to probe; default is %s" % default_spec_file)

    group.add_argument("-B", "--probe-spec", type=str, action='append',
                       help="String specifying ports and protocols to probe; may be repeated.  "
                            "Each string is of the form "
                            "'<port-range>[,<port-range>...][:[<proto>[,<proto>...]]] "
                            "where <port-range> is of the form '<port>[-<port>]'.  "
                            "Examples: '80,443,8080-8088:http,https' specifies probing "
                            "protocols HTTP and HTTPS on ports 80,443, and 8080 through 8088, "
                            "while '6000-6009' specifies probing whether ports 6000 through "
                            "6009 are open (no protocol check).")

    control_port = "auto"
    parser.add_argument("-c", "--control-port", type=str, default=control_port,
                        help="Tor control port; default is %s" % control_port)

    download_dir = "."
    parser.add_argument("-d", "--download-dir", type=str, default=download_dir,
                        help="Directory for downloaded data files; default is %s" % download_dir)

    sentinel_file = "./PROBE_DONE"
    parser.add_argument("-f", "--sentinel-file", type=str, default=sentinel_file,
                        help="Sentinel file created upon completion; default is %s" % sentinel_file)

    parser.add_argument("-i", "--input-file", type=str, default=None,
                        help="Probe history input; default is standard input.")

    download_limit = 100 * 1024
    parser.add_argument("-l", "--download-limit", type=int, default=download_limit,
                        help="Maximum number of bytes (per HS) to download; default is %d" % download_limit)

    max_threads = 10
    parser.add_argument("-n", "--num-threads", type=int, default=max_threads,
                        help="Maximum number of probing threads; default is %d" % max_threads)

    parser.add_argument("-o", "--output_file", type=str, default=None,
                        help="Output file for probe results; default is standard output.")

    probe_timeout = 180.0
    parser.add_argument("-p", "--probe-timeout", type=float, default=probe_timeout,
                        help="Timeout (in seconds) for individual probes.")

    socks_port = "auto"
    parser.add_argument("-s", "--socks-port", type=str, default=socks_port,
                        help="Tor SOCKS port; default is %s" % socks_port)

    tor_data_dir = "/tmp/.tor_hsprobe"
    parser.add_argument("-t", "--tor-data-dir", type=str,
                        default=tor_data_dir,
                        help="Directory for tor state.  If set, the state "
                             "can be reused in subsequent probes; default is %s" % tor_data_dir)

    parser.add_argument("-T", "--clear-tor-data-dir", action="store_true", default=False,
                        help="Clear tor data directory before starting.")

    verbosity = "debug"
    parser.add_argument("-v", "--verbosity", type=str, default=verbosity,
                        help="Minimum log level (independent of Tor logging).  "
                             "Available in ascending order: debug, info, warning, "
                             "error, critical; default is %s" % verbosity)

    tor_cmd = "tor"
    parser.add_argument("-C", "--tor-cmd", type=str, default=tor_cmd,
                        help="Command to launch Tor proxy/controller; default is '%s'." % tor_cmd)

    tor_log_file = "/dev/null"
    parser.add_argument("-F", "--tor-log-file", type=str, default=tor_log_file,
                        help="Tor logging output file; default is %s" % tor_log_file)

    tor_log_level = "err"
    parser.add_argument("-L", "--tor-log-level", type=str, default=tor_log_level,
                        help="Tor logging level; default is %s" % tor_log_level)

    args = parser.parse_args()
    if args:
        args.queue_size = args.num_threads * 3
        if not (args.spec_file or args.probe_spec):
            args.spec_file = default_spec_file

    return args


def launch_tor(args):
    """
    Starts a Tor proxy
    """

    logger.debug("Launching Tor via \"%s\" in directory \"%s\"." % (args.tor_cmd, args.tor_data_dir))

    regex = re.compile(r'(\w+) listener .+ on port (\d+)')
    proc = stem.process.launch_tor_with_config(
        tor_cmd=args.tor_cmd,
        config={
            "SOCKSPort": args.socks_port,
            "ControlPort": args.control_port,
            "DataDirectory": args.tor_data_dir,
            "CookieAuthentication": "1",
            "SafeLogging": "0",
        },
        timeout=None,
        take_ownership=True,
        completion_percent=80,
        init_msg_handler=(lambda line: tor_msg_handler(line, args, regex)),
    )

    args.control_port = int(args.control_port)
    args.socks_port = int(args.socks_port)

    logger.info("Successfully launched Tor (PID=%d, socks_port=%d, control_port=%d)."
                % (proc.pid, args.socks_port, args.control_port))

    return proc


def tor_msg_handler(line, args, regex):
    """
    Monitors initial Tor log for SOCKS and control port info
    (which appears only when configured as "auto"), and re-logs
    all initial Tor log output to the application log.
    """

    m = regex.search(line)
    if m:
        service = m.group(1).lower()
        port = m.group(2)
        if service == "socks":
            args.socks_port = port
        elif service == "control":
            args.control_port = port

    logger.debug("tor log: %s" % line)


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        logger.info("Caught keyboard interrupt.")
        exit(1)
