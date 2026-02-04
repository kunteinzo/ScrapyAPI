#!/bin/bash

# setup venv
function setup_venv() {
  python3 -m venv .venv && \ 
  source .venv/bin/activate && \ 
  pip install -U pip && \ 
  pip install -r requirements.txt
}

# setup nginx conf
function setup_nginx_conf() {
  sudo ln -sL "$PWD/conf.d/*.conf" /etc/nginx/conf.d/
  sudo nginx -t && sudo nginx -s reload
}