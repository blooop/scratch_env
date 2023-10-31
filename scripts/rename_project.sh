#!/bin/bash

find . \( -type d -name .git -prune \) -o \( -type f -not -name 'tasks.json' \) -print0 | xargs -0 sed -i "s/scratch_env/$1/g"

mv scratch_env $1