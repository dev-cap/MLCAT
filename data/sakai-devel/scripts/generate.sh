#!/bin/bash
#script to fetch sakai.devel mailing list archives

#http://mbox.dr-chuck.net/sakai.devel/60200/60201


no=61000
while [ $no -lt 62000 ]
do
    current=$no
    ((next=no+1))
    echo "http://mbox.dr-chuck.net/sakai.devel/$current/$next"
    ((no=no+1))
done
