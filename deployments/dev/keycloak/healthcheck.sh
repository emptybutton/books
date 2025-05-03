#!/bin/bash

exec 3<>/dev/tcp/localhost/9000
echo -e "GET /health HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n" >&3
cat <&3 | grep -qE "HTTP/1.1 200 OK"
