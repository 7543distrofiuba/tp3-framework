# 75.43 - Introducción a los Sistemas Distribuidos
## Trabajo Práctico 3 - SDN

### Prerequisitos
Para correr el TP debemos tener instalado docker y docker-compose. Para instalarlo, pueden chequear la documentación aquí:
- [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [Fedora](https://docs.docker.com/install/linux/docker-ce/fedora/)
- [Mac](https://docs.docker.com/docker-for-mac/install/)

En Mac, `docker-compose` se instala junto con `docker`. En otras plataformas, hay que instalarlos por separado. Pueden encontrar los pasos de instalación aquí:
- [Linux](https://docs.docker.com/compose/install/)

Una vez que `docker` esté instalado, tenemos que descargar la imagen que utilizaremos para generar el contendor. Para esto, debemos correr

    docker pull iwaseyusuke/mininet

### Instalación
Primero debemos clonar el repositorio del TP

    git clone git@github.com:7543distrofiuba/tp3-framework.git
    cd tp3-framework

El TP requiere la libraría `pox` para correr. Esta está incluida como un submodulo del repositorio. Para inicializarla deben correr el siguiente comando.

    git submodule update --init --recursive

Una vez hecho esto, el ambiente ya esta listo para ser ejecutado.

### Directorios

Los archivos necesarios para correr el TP se montan en el contenedor en el directorio `/tmp`. En este directorio pueden encontrar la siguiente estructura

    /tmp
    /tmp/pox -> Aquí se montan los archivos de la libreria pox.
    /tmp/pox/ext -> Aquí se montan los archivos de la carpeta controller. Todo lo que agreguen en este directorio podrá ser ejecutado por pox.
    /tmp/topology -> Aquí se montan los archivos para inicializar las topologías de mininet.
    /tmp/tcpdump -> Aquí se montan la salida de tcpdump para poder capturar tráfico.

### Ejecución

#### Inicializar contenedor

Para ejecutar el ambiente, debemos primero levantar el contenedor de Docker, sobre el cual correremos todos los comandos. Para esto, corremos el siguiente comando.

    docker-compose up -d

#### Controlador Pox

Primero, debemos levantar el controlador `pox`. En este caso, estamos ejecutando un controlador que corre spanning tree.

    docker-compose exec mininet /tmp/pox/pox.py samples.spanning_tree

Para correr sus propios controladores, deben correr

    docker-compose exec mininet /tmp/pox/pox.py <nombre del controlador sin .py>

Por ejemplo, para correr el [controlador de ejemplo](controller/example.py) provisto por la cátedra, debemos ejecutar

    docker-compose exec mininet /tmp/pox/pox.py example

#### Mininet

Para iniciar mininet y levantar la topología tenemos que correr el commando. En este caso, estamos corriendo una topología de ejemplo.

    docker-compose exec mininet mn --custom /tmp/topology/example.py --topo example --mac --arp --switch ovsk --controller remote

Para correr sus propias topologías, deben correr

    docker-compose exec mininet mn --custom /tmp/topology/<archivo de topologia> --topo <nombre de topologia>[,<parametro>] --mac --arp --switch ovsk --controller remote

Una vez que la topología esta iniciada y la consola de mininet esta disponible para utilizar, podemos probar la conexión corriendo

    mininet> h1 ping -c 1 h2
    mininet> pingall

### Capturar Tráfico
Primero, debemos identificar la interfaz a capturar. La interfaz tendra el siguiente formato `sw<N>-eth<M>` en donde N es el número de switch y M es el puerto de salida.

    docker-compose exec mininet ifconfig

Para capturar el tráfico de la interfaz seleccionada, correr el siguiente comando, remplanzando `<interfaz>`

    docker-compose exec mininet tcpdump -C 1000 -v -i <interfaz> -w /tmp/tcpdump/tcpdump.pcap

Por ejemplo, para capturar todas las interfaces, podemos usar

    docker-compose exec mininet tcpdump -C 1000 -v -i any -w /tmp/tcpdump/tcpdump.pcap

Para visualizar los paquetes capturados corremos Wireshark, observando la salida de tcpdump

    tail -c +1 -f tcpdump/tcpdump.pcap | wireshark -k -i -

### Medición del Ancho de Banda
Para medir el ancho de banda de una conexión TCP, tenemos que utilizar la herramienta `iperf` incluida en Mininet. Para medir el ancho de banda entre dos hosts podemos correr el siguiente comando en la consola de mininet

    mininet> iperf h1 h2
    mininet> iperf <nodo1> <nodo2>

Donde cada nodo puede ser un host o un switch.

### Detener ejecución
En caso de necesitarlo, se puede detener la ejecución del contenedor corriendo

    docker-compose down

### Corriendo comandos dentro del container
Otra cosa que también puede ser útil es conectarse al container para correr comandos directamente en ese entorno. Para hacer esto, debemos correr

    docker-compose exec mininet bash

Este comando abre una terminal bash, dentro del container para ejecutar lo que necesitamos.


### Documentación

- [Mininet](http://mininet.org/walkthrough/)
- [POX](https://noxrepo.github.io/pox-doc/html/)
- [Visualizador de Topologías](http://demo.spear.narmox.com/app/?apiurl=demo#!/mininet)
