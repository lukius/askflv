askflv
======

#### Description

This is a Python script to fetch videos from ask.fm.

#### Requirements

 * Python 2.7 + Linux
 * [rtmpdump](http://rtmpdump.mplayerhq.hu) (it can be installed through apt-get on Ubuntu)

#### Usage

Run the askflv.py script specifying one of the following options:
 * <b>-f INPUT_FILE</b>: the program will attempt to parse this file, which should contain valid URLs for ask.fm
  video answers. For every one of these, it will fetch the corresponding video and save it to the file system.
 * <b>-v VIDEO_URL</b>: just download the video located on this single URL.
