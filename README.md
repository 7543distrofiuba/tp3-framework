# mininet-topology
## Setup
After cloning the repo, update the pox submodule

       git submodule update --init --recursive

## Running
Requires docker and docker compose installed

- Run the container: `docker-compose up`
- Run pox: `docker-compose exec mininet /tmp/pox/pox.py samples.spanning_tree`
- Run mininet using one of the provided topos: `docker-compose exec mininet mn --custom /tmp/topology/example.py --topo example --mac --arp --switch ovsk --controller remote`

## Capturing Traffic

- Run tcpdump to capture container's traffic: `docker-compose exec mininet tcpdump -C 1000 -v -i any -w /tmp/tcpdump/tcpdump.pcap`
- Run Wireshark to see the output: `tail -c +1 -f tcpdump/tcpdump.pcap | wireshark -k -i -`

