# FRIBs Voting - Six-Server Model
A cloud voting scheme implemented in FRIBs using the six-server redundancy model. 

## Usage:
1. Create the fragment servers, including new tables.
```
6_Servers> ./setup.sh
```
2. Start each fragment server in a separate session. Note that the three servers need to be started within seconds of each other (a current limitation of this implementation). 
```
6_Servers/bin/server_a> python run_a.py
6_Servers/bin/server_b> python run_b.py
6_Servers/bin/server_c> python run_c.py
6_Servers/bin/server_d> python run_d.py
6_Servers/bin/server_e> python run_e.py
6_Servers/bin/server_f> python run_f.py
```
Sample output for a successful startup is below.
```
```

3. Once the connector closed message has appeared, processing of votes can begin.
4. Use the client to send votes to the fragment servers. In the example below, 157 votes are sent starting at ID 4000.
```
6_Servers/bin/client> python client_many.py 4000 157
```
5. To get the tally result, copy the last output from each fragment server and paste into the following:
```
6_Servers/bin/client> python get_tally_value.py 
```
For example:
```
Please enter the outputs from the three fragment servers (a, b, c, d, e, f).
```
6. Stopping the fragment servers is currently not supported, but the following will work.
```
ps -a | grep "python" | awk '{print $1}' | xargs kill -9
```

## Notes:
- This code is currently for example purposes and it will print the tally each time a vote is added.
- It will also add six zero votes after each pool to make sure the last tally printed is correct, thus flushing the pipeline.
