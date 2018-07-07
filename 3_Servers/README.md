# FRIBs Voting - Three-Server Model
A cloud voting scheme implemented in FRIBs using the three-server enhanced privacy model. 

## Usage:
1. Create the fragment servers, including new tables.
```
3_Servers> ./setup.sh
```
2. Start each fragment server in a separate session. Note that the three servers need to be started within seconds of each other. This is a current limit of this implementation. 
```
3_Servers/bin/server_a> python run_a.py
3_Servers/bin/server_b> python run_b.py
3_Servers/bin/server_c> python run_c.py
```
Sample output for a successful startup is below.
```
Connected
Listen Connected
Listen Connected
scheduler: Server 2 is connected
Connected
scheduler: Server 0 is connected
Connecter closed
```

3. Once the connector closed message has appeared, processing of votes can begin.
4. Use the client to send votes to the fragment servers. In the example below, 157 votes are sent starting at ID 4000.
```
3_Servers/bin/client> python client_many.py 4000 157
```
5. To get the tally result, copy the last output from each fragment server and paste into the following:
```
3_Servers/bin/client> python get_tally_value.py 
```
For example:
```
Please enter the outputs from the three fragment servers (a, b, c).
Fragment server a:
[0, 10, 8, 10, 6, 6]
Fragment server b:
[2, 13, 4, 1, 14, 6]
Fragment server c:
[15, 14, 12, 11, 8, 0]
Tally is 157
```
6. Stopping the fragment servers is currently not supported, but the following will work.
```
ps -a | grep "python" | awk '{print $1}' | xargs kill -9
```

## Notes:
- The fragment servers currently all use the same certificate for network communications.
- This code is currently for example purposes and it will print the tally each time a vote is added.
- It will also add six zero votes after each pool to make sure the last tally printed is correct, thus flushing the pipeline.
