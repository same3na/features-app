#!/bin/bash

# adding the cookies to be used later
#echo "${YOUTUBE_COOKIES}" > /app/src/cookies.txt
# echo "${YOUTUBE_COOKIES}" | base64 -d > /app/src/cookies.txt
service cron start

exec "$@"
