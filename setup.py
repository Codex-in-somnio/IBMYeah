#!/usr/bin/env python3.6
from string import ascii_letters, digits
from json import dump
from hublatest.hublatest import download_repo_release
try:
    from secrets import choice
except ImportError:
    from random import choice


print("Fetching shadowsocks-rust release...")
download_repo_release("shadowsocks", "shadowsocks-rust",
                      download_dir="bin", regex_filter="x86_64-unknown-linux-gnu.tar.xz$",
                      post_download="tar -Jxvf {filepath} -C {filedir};rm {filepath}")
print("Fetching teddysun/v2ray-plugin release...")
download_repo_release("teddysun", "v2ray-plugin",
                      download_dir="bin", regex_filter="linux-amd64",
                      post_download="tar -zxf {filepath} -C {filedir};rm {filepath}")

print("Generating configs...")
with open("config.json", "w") as f:
    password = input("Provide password [default=random]: ")
    if password == '':
        password = password.join(choice(ascii_letters + digits) for i in range(10))
        print("Generated password: \033[7m", password, "\033[0m")
    cipher = input("Provide cipher [default=xchacha20-ietf-poly1305]: ")
    if cipher == '':
        cipher = "xchacha20-ietf-poly1305"
    conf = {
        "server": "0.0.0.0",
        "server_port": 8080,
        "password": password,
        "method": cipher,
        "plugin": "bin/v2ray-plugin_linux_amd64",
        "plugin_opts": "server"
    }
    dump(conf, f)
    f.close()

with open('manifest.yml', 'w') as g:
    name = ''
    while name == '':
        name = input("Provide App name [Required]: ")
    memory = ''
    while memory not in ["64", "128", "256"]:
        memory = input("Provide App memory allocation [64(default)/128/256 without M]: ")
        if memory == '':
            memory = '64'
    route=''
    while route == '':
        route = input("Provide desired route to app [default 'APPNAME.us-east.cf.appdomain.cloud']")
        if route == '':
            route = name + '.us-east.cf.appdomain.cloud'
    manifest = ("applications:\n"
                " - name: {name}\n"
                "   memory: {memory}M\n"
                "   random-route: true\n"
                "   routes:\n"
                "    - route: {route}\n"
                )
    g.write(manifest.format(name=name, memory=memory,route=route))
    g.close()
