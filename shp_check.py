import os
import psycopg2

# Configuring the transport mode to consider
#current_mode = "Train"
#current_mode = "Tram"
current_mode = "Bus"

# Configuration for each mode
train_dict = {"shp_line_in":"out/train_line.shp","shp_stop_in":"out/train_stop.shp","nem_filename_out":"out/train_network.nem"}
train_dict.update({"table_line_out":"nw_train_line","table_point_out":"nw_train_stop"})
train_dict.update({"perform_id_update":False,"mode_abbrev":"T","avg_speed_km_per_hour":40})
tram_dict = {"shp_line_in":"out/tram_line.shp","shp_stop_in":"out/tram_stop.shp","nem_filename_out":"out/tram_network.nem"}
tram_dict.update({"table_line_out":"nw_tram_line","table_point_out":"nw_tram_stop"})
tram_dict.update({"perform_id_update":False,"mode_abbrev":"M","avg_speed_km_per_hour":20})
newnw_dict = {"shp_line_in":"out/network-self-snapped-reworked.shp","shp_stop_in":"out/interchange.shp","nem_filename_out":"out/new_network.nem"}
newnw_dict.update({"table_line_out":"nw_line","table_point_out":"nw_point"})
newnw_dict.update({"perform_id_update":True,"mode_abbrev":"B","avg_speed_km_per_hour":30})
road_dict = {"mode_abbrev":"A"}
mode_dict = {"Train":train_dict,"Tram":tram_dict,"Bus":newnw_dict,"Road":road_dict}

# Assigning variables from the current mode configuration to working variables
nem_filename_out = mode_dict[current_mode]["nem_filename_out"]
shp_line_in  = mode_dict[current_mode]["shp_line_in"]
shp_stop_in = mode_dict[current_mode]["shp_stop_in"]
table_line_out = mode_dict[current_mode]["table_line_out"]
table_point_out = mode_dict[current_mode]["table_point_out"]
perform_id_update = mode_dict[current_mode]["perform_id_update"]
mode_abbrev = mode_dict[current_mode]["mode_abbrev"]
point_prefix = mode_abbrev
avg_speed_km_per_hour = mode_dict[current_mode]["avg_speed_km_per_hour"]

# Other variables
target_srid = str(4326)
db_name = "bze"
db_port = str(54321)


# Processing start - loading the shapefiles into the local database
print "Preparing the shapefile "+shp_line_in+" ..."

# Loading the line shapefile into the database
cmd = "shp2pgsql -W LATIN1 -d -D -I -t 2D -S -s "+target_srid+" "+shp_line_in+" "+table_line_out+" > "+table_line_out+".sql"
print "Executing command: "+cmd
os.system(cmd)

# Loading the result using psql
cmd = "psql -p "+db_port+" -d "+db_name+" -f "+table_line_out+".sql"
print "Executing command: "+cmd
os.system(cmd)

print "Preparing the shapefile "+shp_stop_in+" ..."

# Loading the line shapefile into the database
cmd = "shp2pgsql -W LATIN1 -d -D -I -t 2D -S -s "+target_srid+" "+shp_stop_in+" "+table_point_out+" > "+table_point_out+".sql"
print "Executing command: "+cmd
os.system(cmd)

# Loading the result using psql
cmd = "psql -p "+db_port+" -d "+db_name+" -f "+table_point_out+".sql"
print "Executing command: "+cmd
os.system(cmd)


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
try:
	# The game here is to detect if all lines can be decomposed as successions of nodes
	# And to help perform visual checks to make sure all stops are well and trully connected to the lines

	# Setting the IDs of points right, so that we are sure they have unique IDs
	# This is for visual purposes on the stop layer, because we label the stops with ID
	if perform_id_update:
		print "Step 1"
		sql = "update "+table_point_out+" set id=gid;"
		print sql
		cur.execute(sql)
		conn.commit()

	# Exporting a NEM file based on the lines and points identified
	fo = open(nem_filename_out, "w+")

	# Writing the header
	fo.write("Titel;"+nem_filename_out)
	fo.write(
"""Wertbedeutung;Nachfrage
Linienmodus;0
Verkehrsmittelsumme;1
Meterpropixel;111

Koordinatensystem;0;0;1;1
Koordinatentyp;Kugel

Startmittelpunkt;145.0869274;-37.88879178
Startzoomwert;60179;1E-5
Tortenfaktor;6.879E-6
Zeichenmodus;3
Tortendarstellung;1
BIPMaximalwert;50000
Steuerungsleiste;1
Gitter;1
GraueKanten;1
GestrichelteKanten;1
WeisserHintergrund;0
Punktbeschriftung;1
Punktlagebeschriftung;4
VollerPunktname;1
Language;English

""")

	# Getting all the points to write in the file
	print "Step 2"
	sql = "select gid,st_x(geom) as x,st_y(geom) as y from "+table_point_out
	print sql
	cur.execute(sql)
	rows = cur.fetchall()

	print "Step 2a"
	for row in rows:
		print "Point ID: "+str(row[0])
		fo.write("Punkt;"+point_prefix+str(row[0])+";"+str(row[1])+";"+str(row[2])+";Stop "+point_prefix+str(row[0])+";K;0;0;300;300")
		fo.write("\n")

	# Transport modes
	fo.write("\n")

	for m in mode_dict.keys():
		fo.write("Vmittel;"+str(m)+";"+str(mode_dict[m]["mode_abbrev"])+";1;;;;\n")

	fo.write("\n")

	# Line descriptions
	# Getting all the lines to write in the file
	print "Step 3"
	sql = """
		select l_name,array_to_string(array_agg('"""+point_prefix+"""'||p_id),';') as pt_list
		from
		(select l.name as l_name,p.gid as p_id from
		"""+table_line_out+""" l, """+table_point_out+""" p
		where ST_Distance(p.geom,l.geom)<0.000001
		order by l.name,ST_Line_Locate_point(l.geom,ST_ClosestPoint(l.geom,p.geom))
		) t
		group by l_name
		order by l_name;
	"""
	print sql
	cur.execute(sql)
	rows = cur.fetchall()

	print "Step 3a"
	for row in rows:
		print "Line: "+str(row[0])
		fo.write("Linie;"+str(row[0])+";"+mode_abbrev+";1;rot;0;;;\n")
		fo.write("Verlauf;"+str(row[0])+";"+str(row[1])+";\n")
		fo.write("Halte;"+str(row[0])+";"+str(row[1]))
		fo.write("\n\n")

	# Kanzeit section - time travel = length by average speed
	print "Step 4"
	sql = """
select l_name,'"""+point_prefix+"""'||pt_a as pt_a,'"""+point_prefix+"""'||pt_b as pt_b,
round(st_length(
  st_transform(
    st_line_substring(
      nl.geom,
      ST_Line_Locate_point(nl.geom,ST_ClosestPoint(nl.geom,pa.geom)),
      ST_Line_Locate_point(nl.geom,ST_ClosestPoint(nl.geom,pb.geom))
    )
  ,3111)
)::numeric,0) as leg_length 
from
(
  select l_name,pt_arr[i] as pt_a,pt_arr[i+1] as pt_b 
  from
  (
    select l_name,pt_arr,generate_series(1,array_length(pt_arr,1)-1) as i 
    from
    (
      select l_name,array_agg(p_id) as pt_arr
      from
        (
          select l.name as l_name,p.gid as p_id 
          from """+table_line_out+""" l, """+table_point_out+""" p
          where ST_Distance(p.geom,l.geom)<0.000001
          order by l.name,ST_Line_Locate_point(l.geom,ST_ClosestPoint(l.geom,p.geom))
        ) t
      group by l_name order by l_name
    ) t
  ) s
) u, """+table_point_out+""" pa, """+table_point_out+""" pb, """+table_line_out+""" nl
where pa.gid=u.pt_a and pb.gid=u.pt_b
and ST_Distance(pa.geom,nl.geom)<0.000001
and ST_Distance(pb.geom,nl.geom)<0.000001
and nl.name=u.l_name order by l_name
	"""
	print sql
	cur.execute(sql)
	rows = cur.fetchall()

	print "Step 4a"
	for row in rows:
		print "Edge: "+str(row[1])+" to "+str(row[2])+" on line "+str(row[0])

		# Applying an average speed to the segment length
		# 
		duration_in_sec = int(round(int(row[3])/(avg_speed_km_per_hour*1000.0/3600),0))
		fo.write("Kanzeit;"+str(row[1])+";"+str(row[2])+";A;"+str(duration_in_sec)+"\n")


	fo.write("\n\n")

	# Laegen section: physical length of each edge
	print "Step 5"
	for row in rows:
		print "Edge: "+str(row[1])+" to "+str(row[2])+" on line "+str(row[0])

		# Segment length is already in the 4th attribute
		fo.write("Laenge;"+str(row[1])+";"+str(row[2])+";A;"+str(row[3])+"\n")

	fo.write("\n\n")
	fo.close()

	"""
	# Exporting the line table as a shapefile
	print "Step 6a"	
	cmd = "pgsql2shp -f "+shp_line_in2+" -p "+db_port+" "+db_name+" "+table_line_out
	print "Executing command: "+cmd
	#os.system(cmd)	
	
	# Exporting the point table as a shapefile
	print "Step 6b"	
	cmd = "pgsql2shp -f "+shp_point_in2+" -p "+db_port+" "+db_name+" "+table_point_out
	print "Executing command: "+cmd
	#os.system(cmd)
	"""

except Exception,e: 
    print "I can't do that"
    print str(e)
 