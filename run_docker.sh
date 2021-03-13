#!/bin/bash
docker run -d --name measurement-bot -p 80:80 -p 443:443 --restart=always measurement-bot