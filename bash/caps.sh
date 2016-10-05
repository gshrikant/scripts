#!/usr/bin/env bash

caps_stat="off"
old_stat=$caps_stat

while true;
do
    while read num caps lock stat x;
    do
        caps_stat=$stat     # update
        if [ $caps_stat != $old_stat ];
        then
            old_stat=$caps_stat

            # Notification for 25 ms, with keyboard icon.
            # ${str^^} used to convert $str to uppercase.
            notify-send "Caps Lock" "${caps_stat^^}" -i input-keyboard -t 25
        fi
    done <<< "$(xset -q | grep "Caps Lock")"
done


