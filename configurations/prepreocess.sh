#!/bin/bash

# Note: skeleton for the post processing script
# World size and initial population are fixed to match included examples
datFile=analyze9.dat
cat $datFile | sed 's/world_size32_init50//g' | \ 
  sed 's/_sync/1,/' | \
  sed //'s/_async/0,/' | \ 
  sed 's/_rand_p/1,/g'  | \
  sed 's/_st/,/g' | \
  sed 's/:/,/g'


