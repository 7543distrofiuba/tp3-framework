"""
Este archivo ejemplifica la creacion de una topologia de mininet
En este caso estamos creando una topologia muy simple con la siguiente forma

   host --- switch --- switch --- host
"""

from mininet.topo import Topo

class Example( Topo ):
  def __init__( self, half_ports = 2, **opts ):
    Topo.__init__(self, **opts)

    # Primero creamos los dos switches
    sw1 = self.addSwitch('sw1')
    sw2 = self.addSwitch('sw2')

    # Luego creamos los dos hosts
    h1 = self.addHost('h1')
    h2 = self.addHost('h2')

    """
    Por ultimo, creamos los links para terminar con una topologia con la siguiente forma
    h1 --- sw1 ---- sw2 ---- h2
    """
    self.addLink(sw1, sw2) # Conectando los dos switches
    self.addLink(sw1, h1) # Conectando el sw1 con h1
    self.addLink(sw2, h2) # Conectando el sw2 con h2

topos = { 'example': Example }
