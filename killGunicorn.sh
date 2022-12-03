#!/usr/bin/bash
echo "Stoppo il servizio gunicorn" 
mypid=$(ps xa | grep gunicorn | awk '{ print $1 }' | head -n 1) 
kill $mypid
echo "That's all, folks ;)"
