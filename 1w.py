#!/usr/bin/env python

# This file is part of Openplotter.
# Copyright (C) 2015 by sailoog <https://github.com/sailoog/openplotter>
#
# Openplotter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# any later version.
# Openplotter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Openplotter. If not, see <http://www.gnu.org/licenses/>.

import socket, pynmea2
from w1thermsensor import W1ThermSensor
from classes.conf import Conf

conf=Conf()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sensors_list=eval(conf.get('1W', 'DS18B20'))

sensors=[]
for i in sensors_list:
	sensors.append(W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, i[3]))

while True:
	temp=''
	list_tmp=[]	
	ib=0
	try:
		for i in sensors_list:
 			if i[2]=='C': unit=W1ThermSensor.DEGREES_C
			if i[2]=='F': unit=W1ThermSensor.DEGREES_F
			if i[2]=='K': unit=W1ThermSensor.KELVIN
			temp=sensors[ib].get_temperature(unit)
			
			temp=round(temp,1)
			list_tmp.append('C')
			list_tmp.append(str(temp))
			list_tmp.append(i[2])
			list_tmp.append(i[4])
			ib=ib+1
	except: pass
	
	if list_tmp:
		xdr = pynmea2.XDR('OS', 'XDR', (list_tmp))
		xdr1=str(xdr)
		xdr2=xdr1+"\r\n"
		sock.sendto(xdr2, ('127.0.0.1', 10110))