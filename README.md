NEM tools
=========

This repository contains a set of tools to convert shapefiles to Netview's NEM format, and back.

Pre-requisite:
- a local installation of the OpenGeo Suite (tested on Community Edition 3.02)
- Python interpreter (tested on 2.7.5 for Windows 64-bit)
Note: in Windows, access to the Python executable relies on PYTHONPATH referencing the Python library folder and the PATH variable referencing PYTHONPATH
- the transitfeed Python library (https://code.google.com/p/googletransitdatafeed/wiki/TransitFeedDistribution)
Note: after several unsuccessful attempts at installing the library, it has been added as a submodule of this repository: 
git submodule add git://github.com/drt24/googletransitdatafeed.git gtfs


The tools in this library are:
- shp_prep: cleans up an arbitrary shapefile representing a network into stop-to-stop linestrings. 
The overall visual aspect of the network is maintained. Unique IDs are assigned to linestrings to maintain link throughout the subsequent conversion to NEM format.
- gtfs2shp: a tool to translate a GTFS file into a shapefile.
This is essentially a wrapper around the transitfeed kmlwriter.py followed by an ogr2ogr transformation.
