#!/usr/bin/env python

# usage: mn --custom <path to Example.py> --topo Example[,n] ...

"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host
"""

from mininet.topo import Topo

class Example( Topo ):
    "Example topology"

    def __init__( self, half_ports = 2, **opts ):
        "Create custom topo."

        Topo.__init__(self, **opts)

        sw1 = self.addSwitch('sw1')
        sw2 = self.addSwitch('sw2')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        self.addLink(sw1, sw2)
        self.addLink(sw1, h1)
        self.addLink(sw2, h2)




topos = { 'example': Example }
