# -*- coding: utf-8 -*-

"""
sismosc.py
-------------
Descarga y parsea los registros de http://www.ssn.unam.mx/sismicidad/ultimos/ 
para convertirlos en un stream OSC, periódico.

Uso:
> python sismocs.py col_num osc_host osc_port osc_route send_period, get_period

Argumentos:
	col_num 	<- numero de columna en la tabla que contiene el valor a enviar
	osc_host 	<- dirección ip del host osc
	osc_port 	<- puerto osc
	osc_route 	<- ruta de los mensajes osc
	send_period <- periodo en segundos entre mensaje y mensaje
	get_period 	<- periodo en segundos para volver a cargar el archivo

Ejemplo:
> python sismosc.py 0 192.168.1.73 8000 /magnitud/grados 0.5 60

"""
import OSC, sys, csv
from time import localtime, time, sleep, asctime
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

def get_data():
	try:
		f = open(file_name, "r")
		reader = csv.reader(f)
		rows = [row for row in reader]
		head = rows[0]
		rows = rows[1:]
		print "[._.] :: loaded: ",str(len(rows)), "rows w/", str(len(head)), "columns."
	except:
		print "[+_+] :: no se pudo cargar el archivo", file_name
	return head, rows

def get_net_data():
	try:
		page = mech.open(url)
		html = page.read()
		soup = BeautifulSoup(html)
		ta = soup.find("table")
		# get the head
		h = ta.find('tr')
		cels = h.findAll('th')
		head = [c.text.encode('utf8', 'xmlcharrefreplace') for c in cels]
		# then get the body
		rows = []
		for row in ta.findAll('tr')[1:]:
		    cels = row.findAll('td')
		    record = [c.text.encode('utf8', 'xmlcharrefreplace') for c in cels]
		    rows.append(record)
		print "[._.] :: loaded: ",str(len(rows)), "rows w/", str(len(head)), "columns."
	except:
		print "[+_+] :: no se pudo cargar la URL", url
	return head, rows

def send_osc(val, cOsc):
	msg = OSC.OSCMessage()
	msg.setAddress(route)
	msg.append(val)
	cOsc.send(msg)
	return route+" "+str(val)


if __name__ == "__main__":
	send_period = 1
	osc_host = "127.0.0.1" 
	osc_port = 8000
	mech = Browser()
	url = "http://www.ssn.unam.mx/sismicidad/ultimos/"
		
	# -- args
	if (len(sys.argv)==7):
		col_num = int(sys.argv[1] )
		osc_host = str(sys.argv[2])
		osc_port = int(sys.argv[3])
		route = str(sys.argv[4])
		send_period = float(sys.argv[5])
		get_period = float(sys.argv[6])
		print "[o.o] :: URL_name=%s, COL_num=%d,OSC_host=%s, OSC_port=%d, OSC_route=%s, SEND_period=%0.2f, GET_period=%0.2f" % \
			(url, col_num, osc_host, osc_port, route, send_period, get_period)
	else:
		print "[+.+] :: formato de argumentos incorrecto, use"
		print "       > python csv_to_osc.py file_name col_num osc_host osc_port osc_route send_period, get_period"
	# -- osc
	try:
		send_addr = osc_host, osc_port
		cOsc = OSC.OSCClient()
		cOsc.connect(send_addr)
		print "[._.] :: osc : ok"
	except:
		print "[+_+] :: no se pudo crear la conexión OSC"
	# -- data
	iii = 0;
	head, rows = get_net_data()
	# -- the loop
	t0 = time()
	print u"[._·] :: streaming ::"
	while ( True ):
		# -- stream data
		mms = send_osc(rows[iii][col_num].split(' ')[0], cOsc)
		iii += 1
		if (iii>=len(rows)):
			iii = 0
		print "\t\t[ >>] :: /",iii,"/ :: "+mms
		# -- maybe update
		if ( abs(time()-t0) > get_period ):
			head, rows = get_net_data()
			t0 = time()
		# --sleep	
		sleep(send_period)
	# end whilep