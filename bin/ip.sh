#!/bin/bash

cm cluster nodes > hostlist.txt
cut -d' ' -f2- hostlist.txt > hosts.txt
cut -d' ' -f1 hostlist.txt > hostList.txt

cm cluster inventory > hosts
i=1
echo "[all]"
tail -n +2 hosts | while IFS='' read -r line || [[ -n "$line" ]]; do
	echo "node$1 host=$line"
	i=$((i+1))
done
printf "\n"
echo "[nimbus]"
nimbus=$(sed -n '2p' hosts)
echo "node1 host=$nimbus"
printf "\n"
echo "[supervisors]"
i=2
tail -n +3 hosts | while IFS='' read -r line || [[ -n "$line" ]]; do
	echo "node$i host=$line"
	i=$((i+1))
done

#readarray -t array < hosts.txt
#for host in ${array[@]}
#do
#	scp hosts.txt hostList.txt download.sh setup.sh makeHosts.sh makeZoo.sh makeStorm.sh startZoo.sh startStorm.sh cc@$host:/home/cc/
#	ssh -t cc@$host "echo $host > ip; sudo chmod +x download.sh; sudo chmod +x setup.sh; sudo chmod +x makeZoo.sh; sudo chmod +x makeHosts.sh; sudo chmod +x makeStorm.sh; chmod +x startZoo.sh; chmod +x startStorm.sh"
#done
