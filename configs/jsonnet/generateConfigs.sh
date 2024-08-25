#!/usr/bin/env bash

for j in *.jsonnet ;
    do ( jsonnet $j | yq -P > ../"${j%%.*}".yaml) ;
done