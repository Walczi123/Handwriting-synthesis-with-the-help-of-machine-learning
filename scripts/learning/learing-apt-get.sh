#!/bin/bash

./../../tesseract-training/hardware-dependent/apt-get/train-apt-get.sh &

while :
do
	sleep 30m
    if test `find "notification" -mmin +30`
    then
        sendmail -t < test-mail.txt
    fi
done