#!/bin/zsh
uv run recipes build && rsync -avzu --info=progress2 -h _html/* tonks:/usr/share/webapps/recipes
