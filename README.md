NEM tools
=========

This repository contains a set of tools to convert shapefiles to Netview's NEM format, and back.

Pre-requisites:

- a local installation of the OpenGeo Suite (tested on Community Edition 3.02)

- Python interpreter (tested on 2.7.5 for Windows 64-bit)

Note: in Windows, access to the Python executable relies on PYTHONPATH referencing the Python library folder and the PATH variable referencing PYTHONPATH

- GDAL libray binaries (tested with release-1600-x64-gdal-1-10-mapserver-6-2 downloaded from http://www.gisinternals.com/sdk/Download.aspx?file=release-1600-x64-gdal-1-10-mapserver-6-2.zip)

- the transitfeed Python library (https://code.google.com/p/googletransitdatafeed/wiki/TransitFeedDistribution)

Note: after several unsuccessful attempts at installing the library, it has been added as a submodule of this repository: 
git submodule add git://github.com/drt24/googletransitdatafeed.git gtfs


The tools in this library are:

- shp_prep: cleans up an arbitrary shapefile representing a network into stop-to-stop linestrings. 

The overall visual aspect of the network is maintained. Unique IDs are assigned to linestrings to maintain link throughout the subsequent conversion to NEM format.


- gtfs2shp: a tool to translate a GTFS file into a KML file.

This is a basic wrapper around the transitfeed kmlwriter.py and OGR2OGR commands.

Note: Due to a limitation into how QGIS and the GDAL library handle nested folders having the same name, we introduce a change in kmlwriter.py so that Patterns folders have different names:
-	folder = self._CreateFolder(parent, 'Patterns', visible)
+    # Adding an explicit route name to the Patterns folder name so that QGIS/ogr don't get confused
+    folder = self._CreateFolder(parent, 'Patterns-'+str(route.route_long_name), visible)


- shp2nem: a tool that translate shapefiles for different networks in an aggregated, routable NEM file

This converts a geographically accurate network into a node/edges routable network and several NEM files.
The NEM files have to be manually merged into a single NEM file for multi-modal routing.


