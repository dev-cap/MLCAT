#!/bin/bash

for foldername in *; do
    mkdir $foldername/graphs $foldername/heatmaps $foldername/json $foldername/mbox $foldername/plots $foldername/tables
done
