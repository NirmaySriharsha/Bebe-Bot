#!/bin/bash

# Change to directory
cd tensorflow1/models/research/object_detection

#Run python with testing environment in a new screeen
screen -d -m python bebebot-detector.py
screen -d -m node bebebot-messager.js

