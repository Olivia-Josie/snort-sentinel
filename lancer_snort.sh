#!/bin/bash
sudo snort -i eth0 -R rules/sentinel.rules -A alert_fast -l /var/log/snort -q
