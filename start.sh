#!/usr/bin/env bash
source ./env
./bin/shadowsocks2-linux -s "0.0.0.0:8080" \
  -password "$PASSWD" \
  -cipher "$CIPHER" \
  -plugin "./bin/v2ray-plugin_linux_amd64" \
  -plugin-opts "server"
