import os
import psycopg2


shp_line_in  = "out/network-self-snapped-reworked.shp"
shp_point_in = "out/interchange.shp"
shp_stop_in = "out/stop.shp"

nem_filename_out = "out/new_network.nem"

table_line_out = "nw_line"
table_point_out = "nw_point"
table_stop_out = "nw_stop"

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

print "Preparing the shapefile "+shp_stop_in+" ..."

# Loading the line shapefile into the database
cmd = "shp2pgsql -W LATIN1 -d -D -I -t 2D -S -s "+target_srid+" "+shp_stop_in+" "+table_stop_out+" > "+table_stop_out+".sql"
print "Executing command: "+cmd
os.system(cmd)

# Loading the result using psql
cmd = "psql -p "+db_port+" -d "+db_name+" -f "+table_stop_out+".sql"
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

	# Merging points from the stop dataset into the nw_point
	print "Step 1a"
	sql = "update nw_point set typ='INTERSECT';"
	print sql
	cur.execute(sql)
	conn.commit()

	# Merging points from the stop dataset into the nw_point
	print "Step 1b"
	sql = "insert into nw_point (typ,geom) select 'LINEEND',geom from nw_stop"
	print sql
	cur.execute(sql)
	conn.commit()

	# Setting the IDs of points right, so that we are sure they have unique IDs
	print "Step 1c"
	sql = "update nw_point set id=gid;"
	print sql
	cur.execute(sql)
	conn.commit()

	# Exporting a NEM file based on the lines and points identified
	fo = open(nem_filename_out, "w+")

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
	sql = "select id,st_x(geom) as x,st_y(geom) as y from nw_point"
	print sql
	cur.execute(sql)
	rows = cur.fetchall()

	print "Step 2a"
	for row in rows:
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

	print "Step 3a"
	for row in rows:
		print "Line: "+str(row[0])
		fo.write("Linie;"+str(row[0])+";A;1;rot;0;;;\n")
		fo.write("Verlauf;"+str(row[0])+";"+str(row[1])+";\n")
		fo.write("Halte;"+str(row[0])+";"+str(row[1]))
		fo.write("\n\n")

	# Kanzeit section - time travel = length by average speed
	print "Step 4"
	sql = """
select l_name,'X'||pt_a as pt_a,'X'||pt_b as pt_b,
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
          select l.name as l_name,p.id as p_id 
          from nw_line l, nw_point p
          where ST_Distance(p.geom,l.geom)<0.000001
          order by l.name,ST_Line_Locate_point(l.geom,ST_ClosestPoint(l.geom,p.geom))
        ) t
      group by l_name order by l_name
    ) t
  ) s
) u, nw_point pa, nw_point pb, nw_line nl
where pa.id=u.pt_a and pb.id=u.pt_b
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
		avg_speed_km_per_hour = 20
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
	cmd = "pgsql2shp -f "+shp_point_in2+" -p "+db_port+" "+db_name+" \"SELECT id,geom FROM nw_point WHERE typ='INTERSECT'\""
	print "Executing command: "+cmd
	#os.system(cmd)	

	# Exporting the stop table as a shapefile
	print "Step 6b"	
	cmd = "pgsql2shp -f "+shp_stop_in2+" -p "+db_port+" "+db_name+" \"SELECT id,geom FROM nw_point WHERE typ='LINEEND'\""
	print "Executing command: "+cmd
	#os.system(cmd)	
	"""

except Exception,e: 
    print "I can't do that"
    print str(e)
 