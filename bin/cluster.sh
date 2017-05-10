#!/bin/bash

cm cluster define -n $1 -c $2 --image $3 --flavor $4 -C $5
cm cluster use $1
cm cluster allocate
