import os,sys
import psycopg2

# Database / global variables
target_srid = str(4326)
db_name = "bze"
db_port = str(54321)

# Configuration for each mode
train_dict = {"shp_line_in":"in/shp/train_line.shp","shp_stop_in":"in/shp/train_stop.shp","nem_filename_out":"out/train_network.nem"}
train_dict.update({"table_line_out":"nw_train_line","table_point_out":"nw_train_stop"})
train_dict.update({"perform_id_update":False,"mode_abbrev":"T","avg_speed_km_per_hour":40,"line_color":"blau"})

tram_dict = {"shp_line_in":"in/shp/tram_line.shp","shp_stop_in":"in/shp/tram_stop.shp","nem_filename_out":"out/tram_network.nem"}
tram_dict.update({"table_line_out":"nw_tram_line","table_point_out":"nw_tram_stop"})
tram_dict.update({"perform_id_update":False,"mode_abbrev":"M","avg_speed_km_per_hour":20,"line_color":"gruen"})

newnw_dict = {"shp_line_in":"in/shp/network-self-snapped-reworked.shp","shp_stop_in":"in/shp/interchange.shp","nem_filename_out":"out/new_network.nem"}
newnw_dict.update({"table_line_out":"nw_line","table_point_out":"nw_point"})
newnw_dict.update({"perform_id_update":True,"mode_abbrev":"B","avg_speed_km_per_hour":30,"line_color":"rot"})

road_dict = {"mode_abbrev":"A"}

walk_dict = {"shp_line_in":"","shp_stop_in":"","nem_filename_out":"out/walk_network.nem"}
walk_dict.update({"table_line_out":"nw_walk_line","table_point_out":""})
walk_dict.update({"perform_id_update":False,"mode_abbrev":"W","avg_speed_km_per_hour":5,"line_color":"orange"})

od_dict = {"shp_line_in":"","shp_stop_in":"in/shp/zone_node.shp","nem_filename_out":"out/od_network.nem"}
od_dict.update({"table_line_out":"nw_od_line","table_point_out":"nw_od_point"})
od_dict.update({"perform_id_update":False,"mode_abbrev":"E","avg_speed_km_per_hour":5,"line_color":"rosa"})

mode_dict = {"Train":train_dict,"Tram":tram_dict,"Bus":newnw_dict,"Road":road_dict,"Walk":walk_dict,"OD":od_dict}

if mode_dict.has_key(sys.argv[1]):
	current_mode = sys.argv[1];
else:
	print "Command line argument must be in:"+str(mode_dict.keys())
	sys.exit(0)

# Assigning variables from the current mode configuration to working variables
nem_filename_out = mode_dict[current_mode]["nem_filename_out"]
shp_line_in  = mode_dict[current_mode]["shp_line_in"]
shp_stop_in = mode_dict[current_mode]["shp_stop_in"]
table_line_out = mode_dict[current_mode]["table_line_out"]
table_point_out = mode_dict[current_mode]["table_point_out"]
perform_id_update = mode_dict[current_mode]["perform_id_update"]
mode_abbrev = mode_dict[current_mode]["mode_abbrev"]
line_color = mode_dict[current_mode]["line_color"]
point_prefix = mode_abbrev
avg_speed_km_per_hour = mode_dict[current_mode]["avg_speed_km_per_hour"]

if shp_line_in:
	# Processing start - loading the shapefiles into the local database
	print "Preparing the shapefile "+shp_line_in+" ..."

	# Loading the line shapefile into the database
	cmd = "shp2pgsql -W LATIN1 -d -D -I -t 2D -S -s "+target_srid+" "+shp_line_in+" "+table_line_out+" > tmp/"+table_line_out+".sql"
	print "Executing command: "+cmd
	os.system(cmd)

	# Loading the result using psql
	cmd = "psql -p "+db_port+" -d "+db_name+" -f tmp/"+table_line_out+".sql"
	print "Executing command: "+cmd
	os.system(cmd)

if shp_stop_in:
	print "Preparing the shapefile "+shp_stop_in+" ..."

	# Loading the line shapefile into the database
	cmd = "shp2pgsql -W LATIN1 -d -D -I -t 2D -S -s "+target_srid+" "+shp_stop_in+" "+table_point_out+" > tmp/"+table_point_out+".sql"
	print "Executing command: "+cmd
	os.system(cmd)

	# Loading the result using psql
	cmd = "psql -p "+db_port+" -d "+db_name+" -f tmp/"+table_point_out+".sql"
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

	# Tram stop cleanup: only those stops which are on a line!
	if current_mode == "Tram":
		print "Step 1a"
		sql = """
delete from nw_tram_stop 
where gid in
(select s.gid from nw_tram_stop s 
where not exists 
(select 1 from nw_tram_line l where st_Intersects(s.geom,l.geom)));"""
		print sql
		cur.execute(sql)
		conn.commit()		

	if current_mode == "Walk":
		# Loading resources for differential correspondance walking distances
		shp_zone_in = "in/shp/zone_walk_radius.shp"
		table_zone_out = "zone_access_radius"
		# Processing start - loading the shapefiles into the local database
		print "Preparing the shapefile "+shp_zone_in+" ..."

		# Loading the line shapefile into the database
		cmd = "shp2pgsql -W LATIN1 -d -D -I -t 2D -S -s "+target_srid+" "+shp_zone_in+" "+table_zone_out+" > tmp/"+table_zone_out+".sql"
		print "Executing command: "+cmd
		os.system(cmd)

		# Loading the result using psql
		cmd = "psql -p "+db_port+" -d "+db_name+" -f tmp/"+table_zone_out+".sql"
		print "Executing command: "+cmd
		os.system(cmd)		 


		print "Step 1a"
		sql = "drop table if exists "+table_line_out+";"
		print sql
		cur.execute(sql)
		conn.commit()

		print "Step 1b"
		sql = """
create table """+table_line_out+""" as
select name,pt_a,pt_b,geom
from
(
select 
cast('W-T'||a.gid||'-M'||b.gid as character varying) as name,'T'||a.gid as pt_a,'M'||b.gid as pt_b,
st_makeline(a.geom,b.geom) as geom 
from nw_train_stop a,nw_tram_stop b, zone_access_radius z
where st_distance(st_transform(a.geom,3111),st_transform(b.geom,3111))<z.radius and st_intersects(a.geom,z.geom)
union
select 
cast('W-T'||a.gid||'-B'||b.gid as character varying) as name,'T'||a.gid as pt_a,'B'||b.gid as pt_b,
st_makeline(a.geom,b.geom) as geom 
from nw_train_stop a,nw_point b, zone_access_radius z
where st_distance(st_transform(a.geom,3111),st_transform(b.geom,3111))<z.radius and st_intersects(a.geom,z.geom)
union 
select
cast('W-M'||a.gid||'-B'||b.gid as character varying) as name,'M'||a.gid as pt_a,'B'||b.gid as pt_b,
st_makeline(a.geom,b.geom) as geom 
from nw_tram_stop a,nw_point b, zone_access_radius z
where st_distance(st_transform(a.geom,3111),st_transform(b.geom,3111))<z.radius and st_intersects(a.geom,z.geom)
) t;
		"""
		print sql
		cur.execute(sql)
		conn.commit()


	if current_mode == "OD":
		print "Step 1a"
		sql = "drop table if exists "+table_line_out+";"
		print sql
		cur.execute(sql)
		conn.commit()

		print "Step 1b"
		sql = """
create table """+table_line_out+""" as
select * from
(
select cast('OD-T'||a.gid||'-E'||b.gid as character varying) as name,'T'||a.gid as pt_a,'E'||b.gid as pt_b,
st_makeline(a.geom,b.geom) as geom
from
(select b.gid as od_id,(select a.gid from nw_train_stop a order by st_distance(a.geom,b.geom) limit 1) as stop_id from nw_od_point b) t,
nw_train_stop a,
nw_od_point b
where a.gid=t.stop_id and b.gid=t.od_id and st_distance(st_transform(a.geom,3111),st_transform(b.geom,3111))< 1000
union
select cast('OD-M'||a.gid||'-E'||b.gid as character varying) as name,'M'||a.gid as pt_a,'E'||b.gid as pt_b,
st_makeline(a.geom,b.geom) as geom
from
(select b.gid as od_id,(select a.gid from nw_tram_stop a order by st_distance(a.geom,b.geom) limit 1) as stop_id from nw_od_point b) t,
nw_tram_stop a,
nw_od_point b
where a.gid=t.stop_id and b.gid=t.od_id and st_distance(st_transform(a.geom,3111),st_transform(b.geom,3111))< 1000
union
select
cast('OD-B'||a.gid||'-E'||b.gid as character varying) as name,'B'||a.gid as pt_a,'E'||b.gid as pt_b,
st_makeline(a.geom,b.geom) as geom 
from
(select b.gid as od_id,(select a.gid from nw_point a order by st_distance(a.geom,b.geom) limit 1) as stop_id from nw_od_point b) t,
nw_point a,
nw_od_point b
where a.gid=t.stop_id and b.gid=t.od_id and st_distance(st_transform(a.geom,3111),st_transform(b.geom,3111))< 1000
) u;
		"""
		print sql
		cur.execute(sql)
		conn.commit()


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

	if current_mode != "Walk" and current_mode != "OD":
		# Writing the header
		fo.write("Titel;"+nem_filename_out)
		fo.write("""
Wertbedeutung;Nachfrage
Linienmodus;1
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

		fo.write("\n")
		fo.write("Zeit;1;Ganzer Tag;24;0-24\n")

		# Transport modes
		fo.write("\n")

		for m in mode_dict.keys():
			fo.write("Vmittel;"+str(m)+";"+str(mode_dict[m]["mode_abbrev"])+";1;;;;\n")

		fo.write("\n")


	if current_mode != "Walk":
		# Getting all the points to write in the file
		print "Step 2"
		sql = "select gid,st_x(geom) as x,st_y(geom) as y from "+table_point_out
		print sql
		cur.execute(sql)
		rows = cur.fetchall()

		print "Step 2a"
		for row in rows:
			print "Point ID: "+str(row[0])
			fo.write("Punkt;"+point_prefix+str(row[0])+";"+str(row[1])+";"+str(row[2])+";Stop "+point_prefix+str(row[0])+";H;1000;0;300;300")
			fo.write("\n")

		fo.write("\n")

	# Line descriptions
	# Getting all the lines to write in the file
	print "Step 3"
	if current_mode != "Walk" and current_mode != "OD":
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
	else:
		sql = """
		select name,pt_a||';'||pt_b as pt_list
		from """+table_line_out+"""	order by name
		"""
	print sql
	cur.execute(sql)
	rows = cur.fetchall()

	print "Step 3a"
	for row in rows:
		print "Line: "+str(row[0])
		fo.write("Linie;"+str(row[0])+";"+mode_abbrev+";1;"+line_color+";0;;;\n")
		fo.write("Verlauf;"+str(row[0])+";"+str(row[1])+";\n")
		fo.write("Halte;"+str(row[0])+";"+str(row[1]))
		fo.write("\n\n")

	# Kanzeit section - time travel = length by average speed
	print "Step 4"
	if current_mode != "Walk" and current_mode != "OD":
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
	else:
		sql = """
		select name,pt_a,pt_b,round(st_length(st_transform(geom,3111))::numeric,0) as leg_length
		from """+table_line_out+""" order by name;
		"""
	print sql
	cur.execute(sql)
	rows = cur.fetchall()

	print "Step 4a"
	for row in rows:
		print "Edge: "+str(row[1])+" to "+str(row[2])+" on line "+str(row[0])

		# Applying an average speed to the segment length
		# 
		if current_mode != "OD":
			duration_in_sec = int(round(int(row[3])/(avg_speed_km_per_hour*1000.0/3600),0))
		else:
			# Fixed time for network access
			duration_in_sec = 300

		fo.write("Kanzeit;"+str(row[1])+";"+str(row[2])+";"+mode_abbrev+";"+str(duration_in_sec)+"\n")


	fo.write("\n\n")

	# Laegen section: physical length of each edge
	print "Step 5"
	for row in rows:
		print "Edge: "+str(row[1])+" to "+str(row[2])+" on line "+str(row[0])

		# Segment length is already in the 4th attribute
		fo.write("Laenge;"+str(row[1])+";"+str(row[2])+";"+mode_abbrev+";"+str(row[3])+"\n")

	fo.write("\n\n")
	fo.close()

except Exception,e: 
    print "I can't do that"
    print str(e)
 