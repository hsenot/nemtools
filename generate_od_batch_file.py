import os
import psycopg2

d1 = "C:\Herve\data\od_csv\PT_Demand_Base.csv"
d2 = "C:\Herve\data\od_csv\PVV_DEMAND_Base.csv"
od_csv_file = "out/od.csv"

# Other variables
db_name = "bze"
db_port = str(54321)

# Now playing with the loaded table
try:
	conn_str = "dbname='"+db_name+"' user='postgres' host='localhost' port='"+db_port+"'"
	conn = psycopg2.connect(conn_str)
	if conn:
		print "Now connected to the database"
		# Keeping only the bare minimum table: gid and geom
except:
    print "I am unable to connect to the database"

cur = conn.cursor()
# Exporting a NEM file based on the lines and points identified
fo = open(od_csv_file, "w+")

big_dict = {}

print "Reading file 1 ..."
with open(d1,'r') as f1:
	for line1 in f1:
		# Put the element in a double array (or dict)
		o,d,w = line1.split(',')
		if big_dict.has_key(o):
			if big_dict[o].has_key(d):
				big_dict[o][d] = big_dict[o][d] + w
			else:
				big_dict[o][d] = w
		else:
			big_dict[o]={}
			big_dict[o][d] = w

print "Reading file 2 ..."
with open(d2,'r') as f2:
	for line2 in f2:
		# Put the element in a double array (or dict)
		o,d,w = line2.split(',')
		if big_dict.has_key(o):
			if big_dict[o].has_key(d):
				big_dict[o][d] = float(float(big_dict[o][d]) + float(w))
			else:
				big_dict[o][d] = float(w)
		else:
			big_dict[o]={}
			big_dict[o][d] = float(w)

print "Writing OD CSV file ..."
for o in big_dict.keys():
	for d in big_dict[o].keys():
		if float(big_dict[o][d])>1.0:
			fo.write("E"+str(o)+";E"+str(d)+";From E"+str(o)+";To E"+str(d)+";1;1\n")

fo.write("\n")
fo.close()

 