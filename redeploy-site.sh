#!/bin/bash
systemctl stop myportfolio
cd /mlh-portfolio
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
systemctl start myportfolio