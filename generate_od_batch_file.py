import os
import psycopg2

# Value under which an OD pair will not be written to the batch file to submit to Netview
# i.e. minimum traffic volume for an OD pair to be considered
weight_threshold = 5.0

# Files, in and out
d1 = "C:\Herve\data\od_csv\PT_Demand_Base.csv"
d2 = "C:\Herve\data\od_csv\PVV_DEMAND_Base.csv"

# still to do: write several OD CSVs (batches of X OD pairs i.e. OD=10,000)
od_csv_file = "out/od.csv"

# Database variables
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
# retrieving a dictionary of OD points that are disconnected from the network so they should not be allowed in the Netview OD routing batch file
print "Step 1"
sql = """
select gid from nw_od_point odp where odp.geom not in 
(
select ST_StartPoint(odl.geom) from nw_od_line odl
union
select ST_EndPoint(odl.geom) from nw_od_line odl
);"""
print sql
cur.execute(sql)
rows = cur.fetchall()

od_pt_to_exclude = {}

print "Step 1a"
for row in rows:
	print "OD point to exclude: "+str(row[0])
	od_pt_to_exclude["E"+str(row[0])]=True

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
	# If the OD has been flagged as "to exclude" we do nothing
	if not od_pt_to_exclude.has_key("E"+str(o)):
		for d in big_dict[o].keys():
			# If the OD has been flagged as "to exclude" we do nothing
			if not od_pt_to_exclude.has_key("E"+str(d)):
				if float(big_dict[o][d])>weight_threshold:
					fo.write("E"+str(o)+";E"+str(d)+";From E"+str(o)+";To E"+str(d)+";1;1\n")

fo.write("\n")
fo.close()

 