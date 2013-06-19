import os
import psycopg2

shp_line_in  = "out/network-self-snapped-reworked.shp"
shp_point_in = "out/interchange.shp"

table_line_out = "nw_line"
table_point_out = "nw_point"

target_srid = str(4326)
db_name = "bze"
db_port = str(54321)

print "Preparing the shapefile "+shp_line_in+" ..."

# Loading the line shapefile into the database
cmd = "shp2pgsql -W LATIN1 -d -D -I -t 2D -S -s "+target_srid+" "+shp_line_in+" "+table_line_out+" > "+table_line_out+".sql"
print "Executing command: "+cmd
os.system(cmd)

# Loading the result using psql
cmd = "psql -p "+db_port+" -d "+db_name+" -f "+table_line_out+".sql"
print "Executing command: "+cmd
os.system(cmd)

print "Preparing the shapefile "+shp_point_in+" ..."

# Loading the line shapefile into the database
cmd = "shp2pgsql -W LATIN1 -d -D -I -t 2D -S -s "+target_srid+" "+shp_point_in+" "+table_point_out+" > "+table_point_out+".sql"
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
	print "Step 1"
	sql = "update nw_point set id=gid;"
	print sql
	cur.execute(sql)
	conn.commit()

	# Exporting a NEM file based on the lines and points identified
	fo = open("test.nem", "w+")

	# Writing the header
	fo.write(
"""
Titel;Test
Wertbedeutung;Nachfrage
Linienmodus;0
Verkehrsmittelsumme;1
Meterpropixel;111

Koordinatensystem;0;0;1;1
Koordinatentyp;Kugel

Startmittelpunkt;133.8981677;-25.50912931
Startzoomwert;1346.2;1E-5
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
	sql = "select id,st_x(geom) as x,st_y(geom) as y from nw_point"
	print sql
	cur.execute(sql)
	rows = cur.fetchall()

	for row in rows:
		print "Step 2a"
		print "Point ID: "+str(row[0])
		fo.write("Punkt;X"+str(row[0])+";"+str(row[1])+";"+str(row[2])+";Intersection "+str(row[0])+";K;0;0;300;300")
		fo.write("\n")

	# Transport modes
	fo.write("\n")
	fo.write("Vmittel;Road;A;1;;;;\n")
	fo.write("\n")

	# Line descriptions
	# Getting all the lines to write in the file
	print "Step 3"
	sql = """
		select l_name,array_to_string(array_agg('X'||p_id),';') as pt_list
		from
		(select l.name as l_name,p.id as p_id from
		nw_line l, nw_point p
		where ST_Distance(p.geom,l.geom)<0.000001
		order by l.name,ST_Line_Locate_point(l.geom,ST_ClosestPoint(l.geom,p.geom))
		) t
		group by l_name
		order by l_name;
	"""
	print sql
	cur.execute(sql)
	rows = cur.fetchall()

	for row in rows:
		print "Step 3a"
		print "Point ID: "+str(row[0])
		fo.write("Linie;"+str(row[0])+";A;1;rot;0;;;\n")
		fo.write("Verlauf;"+str(row[0])+";"+str(row[1])+";\n")
		fo.write("Halte;"+str(row[0])+";"+str(row[1]))
		fo.write("\n\n")

	fo.close()

	# Exporting the line table as a shapefile
	print "Step 6a"	
	cmd = "pgsql2shp -f "+shp_line_in+" -p "+db_port+" "+db_name+" "+table_line_out
	print "Executing command: "+cmd
	#os.system(cmd)	
	
	# Exporting the point table as a shapefile
	print "Step 6b"	
	cmd = "pgsql2shp -f "+shp_point_in+" -p "+db_port+" "+db_name+" "+table_point_out
	print "Executing command: "+cmd
	#os.system(cmd)	

except Exception,e: 
    print "I can't do that"
    print str(e)
 