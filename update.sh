#!/bin/zsh
recipes build && rsync -avzu --info=progress2 -h _html/* tonks:/usr/share/webapps/recipes # && travel social
