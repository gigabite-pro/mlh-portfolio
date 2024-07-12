#!/bin/bash

echo "TESTING GET REQUEST"
curl http://localhost:5000/api/timeline_post

echo "TESTING POST REQUEST"
curl --location 'http://localhost:5000/api/timeline_post' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'name=Vaibhav' \
--data-urlencode 'email=vs301vs@gmail.com' \
--data-urlencode 'content=Just Added Database to my Portfolio site!'

echo "TESTING GET REQUEST AGAIN"
curl http://localhost:5000/api/timeline_post