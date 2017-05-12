Role Name
=========

Automating the deployment of a Storm Cluster

Requirements
------------
For the successful installation of Storm cluster we need an inventory file which has node information, after creating a cluster, in the following format:

    [chameleon]
    node1 ansible_host=129.114.111.46 host=vasmethk-056 ansible_user=cc
    node2 ansible_host=129.114.32.192 host=vasmethk-057 ansible_user=cc
    node3 ansible_host=129.114.33.10 host=vasmethk-058 ansible_user=cc
    node4 ansible_host=129.114.33.151 host=vasmethk-059 ansible_user=cc
    node5 ansible_host=129.114.33.138 host=vasmethk-060 ansible_user=cc
    
    
However, the above has been successfully automated by using hosts.sh script file present in the bin folder, which does the job for us.




Role Variables
--------------
A Role Variables of cloud="cloud" is required to specify which cloud we intend to use.

Dependencies
------------

No dependencies

Example Playbook
----------------

ansible-playbook main.yml --extra-vars "cloud=chameleon"

OR

ansible-playbook:

    ---
    - hosts: cluster
    - become: True
    - roles:
        - cloudmesh.storm

License
-------

BSD

Author Information
------------------

Vasanth Methkupalli(mvasanthiiit@gmail.com)
Ajit Balaga(skynite9@gmail.com)
