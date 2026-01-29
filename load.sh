#!/bin/bash

ln -sLf "$PWD/hellohost.tz.conf" /etc/nginx/conf.d/
nginx -t && nginx -s reload