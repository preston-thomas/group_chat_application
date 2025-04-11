# Slack Lite
* Created by: Preston Thomas & Evan Gronewold

# Run Instructions
* **NOTE: This is assuming you have already fetched the remote repository on the GVSU RDPs**
* VPN into GVSU's network
* Run the following in the terminal: ssh userid@eos<##>.cis.gvsu.edu
* CD to the directory where the server.py script is located (example command: cd /cis457/cis457_group_chat/src
* Run the script (python3 server.py)
* On your local machine, open a new terminal window and enter: ssh -N -L 5000:localhost:5000 userid@eos<##>.cis.gvsu.edu
* To open the client, open another new terminal window (or run in VS Code, but since we will probably be presenting solo, terminal will be easiest to open multiple client sessions)
* CD to the directory on your local machine where the repository's src folder is located
* Run the client: python3 client.py
* Open as many clients as required for the demo and begin chatting!
