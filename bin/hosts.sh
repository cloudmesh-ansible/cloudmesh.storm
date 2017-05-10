#!/bin/bash

cm cluster inventory > hosts.txt
i=1
echo "[cluster]" > hosts
tail -n +2 hosts.txt | while IFS='' read -r line || [[ -n "$line" ]]; do
	echo "node$i host=$line" >> hosts
	i=$((i+1))
done
printf "\n" >> hosts
echo "[nimbus]" >> hosts
nimbus=$(sed -n '2p' hosts.txt)
echo "node1 host=$nimbus" >> hosts
printf "\n" >> hosts
echo "[supervisors]" >> hosts
i=2
tail -n +3 hosts.txt | while IFS='' read -r line || [[ -n "$line" ]]; do
	echo "node$i host=$line" >> hosts
	i=$((i+1))
done
