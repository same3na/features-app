#!/bin/bash

# adding the cookies to be used later
echo "${YOUTUBE_COOKIES}" > /app/src/cookies.txt

exec "$@"