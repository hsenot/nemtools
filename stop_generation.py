import os
import psycopg2

shp_in = "out/new-network-self-snapped.shp"
shp_out = "out/new-intersection.shp"
table_in = "newnw_mini"
table_out = "newnw_point"
target_srid = str(4326)
db_name = "bze"
db_port = str(5432)

print "Preparing the shapefile "+shp_in+" ..."

# Loading the shapefile into the database
cmd = "/usr/lib/postgresql/9.2/bin/shp2pgsql -W LATIN1 -d -D -I -t 2D -S -s "+target_srid+" "+shp_in+" "+table_in+" > "+table_in+".sql"
print "Executing command: "+cmd
os.system(cmd)

# Loading the result using psql
cmd = "sudo -u postgres psql -p "+db_port+" -d "+db_name+" -f "+table_in+".sql"
print "Executing command: "+cmd
os.system(cmd)

# Now playing with the created table
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
	# Dropping minified table
	print "Step 1"
	sql = "DROP TABLE IF EXISTS "+table_out+" CASCADE;"
	print sql
	cur.execute(sql)
	conn.commit()

	# Recreating minified table as a grid-snapped version
	print "Step 2a"
	sql = "CREATE TABLE "+table_out+""" AS
select 
cast(row_number() OVER (ORDER BY gt) as integer) AS id,
the_geom from
(
SELECT ST_StartPoint(ST_Intersection(n1.geom, n2.geom)) as the_geom,
GeometryType(ST_Intersection(n1.geom, n2.geom)) as gt
from newnw_mini n1, newnw_mini n2
where ST_Intersects(n1.geom, n2.geom) and n1.gid > n2.gid
and GeometryType(ST_Intersection(n1.geom, n2.geom)) in ('LINESTRING')
union
SELECT ST_EndPoint(ST_Intersection(n1.geom, n2.geom)) as the_geom,
GeometryType(ST_Intersection(n1.geom, n2.geom))
from newnw_mini n1, newnw_mini n2
where ST_Intersects(n1.geom, n2.geom) and n1.gid > n2.gid
and GeometryType(ST_Intersection(n1.geom, n2.geom)) in ('LINESTRING')
union
SELECT ST_StartPoint(geom),
GeometryType(geom)
from newnw_mini
union
SELECT ST_EndPoint(geom),
GeometryType(geom)
from newnw_mini
union
SELECT ST_Intersection(n1.geom, n2.geom) as the_geom,
GeometryType(ST_Intersection(n1.geom, n2.geom))
from newnw_mini n1, newnw_mini n2
where ST_Intersects(n1.geom, n2.geom) and n1.gid > n2.gid
and GeometryType(ST_Intersection(n1.geom, n2.geom)) in ('POINT')
) s"""
	print sql
	cur.execute(sql)
	conn.commit()

	# Added PK
	print "Step 2b"
	sql = "ALTER TABLE "+table_out+" ADD CONSTRAINT "+table_out+"_pk PRIMARY KEY(id);"
	print sql
	cur.execute(sql)
	conn.commit()

	# Exporting the network as a shapefile
	print "Step 6"	
	cmd = "/usr/lib/postgresql/9.2/bin/pgsql2shp -f "+shp_out+" -p "+db_port+" -u postgres "+db_name+" "+table_out
	print "Executing command: "+cmd
	os.system(cmd)	

except Exception,e: 
    print "I can't do that"
    print str(e)
 