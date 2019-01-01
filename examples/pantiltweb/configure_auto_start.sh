#!/bin/sh
#
# configures systemd to auto start pantilt-flask


cat <<EOF >>/lib/systemd/system/pantilt.service 
[Unit]
Description=pan-tilt webserver
After=multi-user.target

[Service]
ExecStart=/usr/bin/python /home/pi/git/pantilt-hat/examples/pantiltweb/pantilt-flask.py
User=pi

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable pantilt.service
