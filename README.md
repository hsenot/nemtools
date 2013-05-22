NEM tools
=========

This repository contains a set of tools to convert shapefiles to Netview's NEM format, and back.

Pre-requisite:
- a local installation of the OpenGeo Suite (tested on Community Edition 3.02)
- Python interpreter (tested on 2.7.5 for Windows 64-bit)

The tools in this library are:
- shp_prep: cleans up an arbitrary shapefile representing a network into stop-to-stop linestrings. 
The overall visual aspect of the network is maintained. Unique IDs are assigned to linestrings to maintain link throughout the subsequent conversion to NEM format.
