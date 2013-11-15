#!/usr/bin/python

import os
import re
import urllib
import urllib2

from argparse import ArgumentParser


class WebpageRetriever(object):
    
    @classmethod
    def for_url(cls, url):
        return cls(url)
    
    def __init__(self, url):
        self.url = url
        
    def run(self):
        return urllib2.urlopen(self.url).read()


class RTMPDumpCommand(object):

    def set_output(self, output):
        self.output = output
        
    def set_server_url(self, url):
        self.server_url = url
                
    def set_port(self, port):
        self.port = port

    def set_application(self, application):
        self.application = application
                
    def set_player(self, player):
        self.player = player
        
    def set_playpath(self, playpath):
        self.playpath = playpath
        
    def text(self):
        command_template = 'rtmpdump -r %s -a %s -c %d -y %s -W %s -o %s -q'
        return command_template % (self.server_url, self.application, 
                                   self.port, self.playpath, self.player,
                                   self.output)      


class AskVideoDumper(object):    
    
    @classmethod
    def for_url(cls, url):
        return cls(url)
    
    def __init__(self, url):
        self.url = url
        
    def build_rtmpdump_command(self, output_filename):
        command = RTMPDumpCommand()
        command.set_output(output_filename)
        command.set_server_url('rtmp://su0wjemth7nht.cloudfront.net')
        command.set_port(1935)
        command.set_application('cfx/st')
        command.set_player('http://ask.fm/objects/flowplayer.rtmp-3.2.3.swf')
        playpath = self.get_video_playpath()
        command.set_playpath(playpath)
        return command.text()
    
    def get_video_playpath(self):
        playpath_regex = re.compile('this, &quot;(.*p_video_answer.*?)&quot;')
        html = WebpageRetriever.for_url(self.url).run()
        matches = playpath_regex.findall(html)
        return matches[0]
        
    def run(self, output_filename):
        try:
            command = self.build_rtmpdump_command(output_filename)
            os.system(command)
        except Exception, e:
            print 'Failed to dump %s! %s' % (self.url, str(e))
            
            
class Main(object):
    
    DESCRIPTION = 'ask.fm video downloader'
    FILE_HELP = 'Input file where ask.fm video URLs are contained'
    VIDEO_URL_HELP = 'Single ask.fm video URL'
    
    def parse_cmdline(self):
        parser = ArgumentParser(description=self.DESCRIPTION)
        
        group = parser.add_argument_group('arguments')
        
        group.add_argument('-f', '--file',
                           action='store', dest='input_file', default='',
                           type=str, help=self.FILE_HELP)
        
        group.add_argument('-v', '--video-url',
                           action='store', dest='video_url', default='',
                           type=str, help=self.VIDEO_URL_HELP)  
        
        options = parser.parse_args()
    
        if not options.input_file and not options.video_url:
            parser.error('must provide input file or video URL')
            
        return options

    def run(self):
        options = self.parse_cmdline()
        if options.input_file:
            self.run_for_file(options.input_file)
        else:
            self.run_for_url(options.video_url)
            
    def run_for_file(self, filename):
        try:
            content = open(filename, 'r').read()
        except Exception, e:
            print 'Failed to read input file! %s' % str(e)
            return
        
        url_regex = re.compile('((http://)?(www\.)?ask\.fm/.*?/answer/\d+)')
        matches = url_regex.findall(content)
        for match in matches:
            video_url = match[0]
            self.run_for_url(video_url)
            
    def run_for_url(self, url):
        output_regex = re.compile('ask\.fm/(.*?)/answer/(\d+)')
        match = output_regex.findall(url)[0]
        output_filename = '%s_%s.flv' % match
        print 'Processing %s - dumping to %s' % (url, output_filename)
        AskVideoDumper.for_url(url).run(output_filename)
            
            
if __name__ == '__main__':
    Main().run()