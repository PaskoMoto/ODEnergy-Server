# ODEnergy-Server
Servidor Python para dispositivos ODEnergy con versión de protocolo ODENERGY 1.0

Las características del proceso son las siguientes:

Se actualizan periódicamente tres ficheros con la información de las tramas recibidas del equipo de medida (ODENERGY Home WiFi).
El primer fichero (PW.csv) contiene información de tramas de consumos medios y se actualiza cada 15 minutos
El segundo fichero (EV.csv) contiene información de tramas de eventos y se actualiza unos minutos después de producirse los eventos.
El tercer fichero (ST.csv) contiene la infromación de las tramas que se generan cada 60 minutos con información de consumos acumulados.

El proceso servidor escucha en el puerto tcp 1730 de manera ininterrumpida. es necesario configurar el dispositivo de medida para que se conecte a la dirección IP sobre la que se ejecuta el proceso de escucha.

El proceso servidor está basado en el ejemplo publicado por el distribuidor del equipo de medida, pero permite almacenar los distintos tipos de tramas de manera separada y acumulando largos periodos de tiempo.

La descripción de las tramas y el protocolo puede encontrarse en el wiki del distribuidor del equipo de medida:
http://www.opendomo.com/wiki/index.php/ODEnergyProtocol


