NEM tools
=========

This repository contains a set of tools to convert shapefiles to Netview's NEM format, and back.

Pre-requisites:

- a local installation of the OpenGeo Suite (tested on Community Edition 3.02)

A database named 'bze', created empty on a PostGIS UTF8 template is assumed in the script.

Download PostGIS (PostgreSQL with GIS extensions) from http://postgis.net/install/.
This page also includes instructions for enabling the PostGIS extensions once
you set up your database.

(A good tool for managing Postgres databases is pgAdminIII. 
Get it from : http://www.pgadmin.org/download/index.php
)


- Python interpreter (tested on 2.7.5 for Windows 64-bit)

Note: in Windows, access to the Python executable relies on PYTHONPATH referencing the Python library folder and the PATH variable referencing PYTHONPATH
Note: in some systems, QGIS might interfere with the newly installed Python. Removing PYTHONPATH from the environment variables has worked in some cases.

- the transitfeed Python library (https://code.google.com/p/googletransitdatafeed/wiki/TransitFeedDistribution)

Note: after several unsuccessful attempts at installing the library, it has been added as a submodule of this repository: 
git submodule add git://github.com/drt24/googletransitdatafeed.git gtfs


- the psycog Python library

Note: on MacOS, it could be as easy as: easy_install psycopg2 (based on http://initd.org/psycopg/install/). You may want to use virtualenv for cleaner library management.
Note: on Windows, the installation of this library might unleash dependency hell. Were helpful to overcome this:
Download and install setup tools (which will allow for the use of easy_install.exe)
Put the OpenGeo Suite pg_config.exe in the PATH
Follow: http://stackoverflow.com/questions/2817869/error-unable-to-find-vcvarsall-bat
which boils down to installing MingW (download from: http://sourceforge.net/projects/mingw/?source=dlp)
The final error points at a flag (mno-cygwin) which is deprecated from latest versions of MingW. Solution here:
http://stackoverflow.com/questions/6034390/compiling-with-cython-and-mingw-produces-gcc-error-unrecognized-command-line-o
Hell exited sucessfully!

- GDAL libray binaries (tested with release-1600-x64-gdal-1-10-mapserver-6-2 downloaded from http://www.gisinternals.com/sdk/Download.aspx?file=release-1600-x64-gdal-1-10-mapserver-6-2.zip)




The tools in this repository are:


- shp2nem: a tool that translate shapefiles for different networks in an aggregated, routable NEM file

On Windows: shp2nem.bat
On *nix systems: shp2nem.sh

This converts a geographically accurate network into a node/edges routable network and several NEM files.
The NEM files have to be manually merged into a single NEM file for multi-modal routing.


- gtfs2shp.py: a tool to translate a GTFS file into a KML file.

This is a basic wrapper around the transitfeed kmlwriter.py and OGR2OGR commands.

Note: Due to a limitation into how QGIS and the GDAL library handle nested folders having the same name, we introduce a change in kmlwriter.py so that Patterns folders have different names:
D-	folder = self._CreateFolder(parent, 'Patterns', visible)
A+    # Adding an explicit route name to the Patterns folder name so that QGIS/ogr don't get confused
A+    folder = self._CreateFolder(parent, 'Patterns-'+str(route.route_long_name), visible)


- shp_prep.py: cleans up an arbitrary shapefile representing a network into stop-to-stop linestrings. 

The overall visual aspect of the network is maintained. Unique IDs are assigned to linestrings to maintain link throughout the subsequent conversion to NEM format.
It is not envisaged that this tool will be (re)used, the code is just captured for historical archiving.
