*CSV_to_OSC*

Herramientas en python y R para crear un stream osc con los datos servicio sismológico nacional, recuperados periodicamente del portal http://www.ssn.unam.mx/sismicidad/ultimos/.
Ejecutar primero temporizador.R para comenzar la descarga periodica de datos, luego csv_to_osc.py para crear el stream.

1. getSismos.R :: descarga, parsea los datos,  y genera el archivo .csv con una tabla
2. temporizador.R	:: crea una tarea en el taskmanager para ejecutar el script anterior periodicamente
3. csv_to_osc.py :: genera un stream osc con los datos del archivo .csv especificados
 
Uso:

    > python csv_to_osc.py file_name col_num osc_host osc_port osc_route send_period get_period
Ejemplo:

    > python csv_to_osc.py sismos.csv 4 192.168.0.12 8000 /profundidad/kms 0.1 60

El script enviara los datos de la quinta columna (los indices comienzan en 0) del archivo sismos.csv como mensajes osc con la ruta /profundidad/kms al puerto 8000 de la dirección ip 192.168.0.12, cada 0.1 segundos, y recarga los datos del archivo cada 60 segundos.
