# ======================================================
# Name: iperf_check_logger.py
# Date: 2023-06-01_1500
# Description: iperf3 to syslog script
# Tested on: Ubuntu Server 22.04.2 LTS
# ======================================================
# Install Prereqs - 'apt install python3 iperf3 pip'
# Install iPerf3 Python Wrapper - 'pip install iperf3'
# ======================================================

# import modules
from logging import getLogger, Formatter
import logging.handlers
import iperf3
import sys

# set variables
# remote iperf3 server
remote_site = sys.argv[1]
# iperf3 port to use
test_port = sys.argv[2]
# length of iperf3 test in seconds
test_duration = 20

# iperf3 setting
# run 10 parallel streams for duration w/ reverse
client = iperf3.Client()
client.server_hostname = remote_site
client.zerocopy = True
client.verbose = False
client.reverse = True
client.port = test_port
client.num_streams = 10
client.duration = int(test_duration)
client.bandwidth = 1000000000

# run iperf3 test
result = client.run()

# extract data from results
iperf_error = result.error
sent_mbps = int(result.sent_Mbps)
received_mbps = int(result.received_Mbps)

# prepare results
iperf_result = f'{remote_site},{test_port},{sent_mbps},{received_mbps}'

# syslog settings
# format string for syslog
log_format = f"%(levelname)s:%(filename)s:%(lineno)d - %(asctime)s - %(message)s"
# get the root logger
logger = getLogger()
# set remote syslog server
syslogHandler = logging.handlers.SysLogHandler(address=("192.168.0.55",5514))
# import format string for the handler
syslogHandler.setFormatter(Formatter(log_format))

# send results
logger.addHandler(syslogHandler)
logger.log(249,iperf_error)
logger.log(250,iperf_result)
