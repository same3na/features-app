#!/bin/bash
# Delete .wav files older than 15 minutes in /tmp
find /tmp -type f -name "*.wav" -mmin +15 -delete