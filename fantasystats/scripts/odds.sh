#!/usr/bin/env bash
PYTHONPATH=/opt/fantasystats python3 /opt/fantasystats/fantasystats/services/crawlers/rotogrinders.py
PYTHONPATH=/opt/fantasystats python3 /opt/fantasystats/fantasystats/scripts/cache.py
