#!/usr/bin/env python3
from string import ascii_letters, digits
from secrets import choice
from hublatest.hublatest import download_repo_release
# Fetching binaries from GitHub release (Powered by HubLatest)
download_repo_release("shadowsocks", "go-shadowsocks2",
                      download_dir="bin", regex_filter="linux",
                      post_download="gzip -fd {filepath};chmod +x {filedir}/shadowsocks2-linux")
download_repo_release("shadowsocks", "v2ray-plugin",
                      download_dir="bin", regex_filter="linux-amd64",
                      post_download="tar -zxf {filepath} -C {filedir};rm {filepath}")
# Generating env file
with open("env", "w") as f:
    password = input("Provide password or default to random:\n")
    if password is '':
        password = password.join(choice(ascii_letters + digits) for i in range(10))
        print("Generated password: ", password)
    f.write("PASSWD=" + password + "\n")
    cipher = input("Provide cipher or default to AEAD_CHACHA20_POLY1305 a.k.a chacha20-ietf-poly1305:\n")
    if cipher is '':
        cipher = "AEAD_CHACHA20_POLY1305"
    f.write("CIPHER=" + cipher + "\n")
    f.close()