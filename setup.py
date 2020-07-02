#!/usr/bin/env python3
from string import ascii_letters, digits
from hublatest.hublatest import download_repo_release
try:
    from secrets import choice
except ImportError:
    from random import choice


# Fetching binaries from GitHub release (Powered by HubLatest)
print("Fetching go-shadowsocks2 release...")
download_repo_release("shadowsocks", "go-shadowsocks2",
                      download_dir="bin", regex_filter="linux",
                      post_download="gzip -fd {filepath};chmod +x {filedir}/shadowsocks2-linux")
print("Fetching v2ray-plugin release...")
download_repo_release("shadowsocks", "v2ray-plugin",
                      download_dir="bin", regex_filter="linux-amd64",
                      post_download="tar -zxf {filepath} -C {filedir};rm {filepath}")

# Generating env file
print("Generating configs...")
with open("env", "w") as f:
    password = input("Provide password [default=random]: ")
    if password is '':
        password = password.join(choice(ascii_letters + digits) for i in range(10))
        print("Generated password: \033[7m", password, "\033[0m")
    cipher = input("Provide cipher [default=AEAD_CHACHA20_POLY1305 a.k.a chacha20-ietf-poly1305]: ")
    if cipher is '':
        cipher = "AEAD_CHACHA20_POLY1305"
    env = ("PASSWD={password}\n"
           "CIPHER={cipher}")
    f.write(env.format(password=password, cipher=cipher))
    f.close()

with open("manifest.yml", "w") as g:
    name = ''
    while name is '':
        name = input("Provide App name [Required]: ")
    memory = ''
    while memory not in ["64", "128", "256"]:
        memory = input("Provide App memory allocation [64(default)/128/256 without M]: ")
        if memory is '':
            memory = "64"
    manifest = ("applications:\n"
                " - name: {name}\n"
                "   random-route: true\n"
                "   memory: {memory}M\n")
    g.write(manifest.format(name=name, memory=memory))
    g.close()
