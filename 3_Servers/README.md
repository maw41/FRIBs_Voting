# FRIBs Voting - Three-Server Model
A cloud voting scheme implemented in FRIBs using the three-server enhanced privacy model. 

## Usage:
1. Create the fragment servers, including new tables.
```
3_Servers> ./setup.sh
```
2. Start each fragment server in a separate session. 
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

3. Processing of votes can begin once a prompt on each fragment server appears.
```
#>
```
4. Use the client to send votes to the fragment servers. In the example below, 157 votes are sent starting at ID 4000.
```
3_Servers/bin/client> python client_many.py 4000 157
Please enter your vote for 157 voters (y/n): y
```
5. To get the tally results, on each server run:
```
#> print tally
Number of votes: 157
Tally: [14, 15, 7, 5, 11, 9]
```
Note that it is safer to flush the tally first, in order to flush the pipeline.
```
#> flush tally
```
But this needs to be done on all fragment servers.

6. Copy the tallies from each fragment server and paste into the following:
```
3_Servers/bin/client> python get_tally_value.py 
```
For example:
```
Please enter the outputs from the three fragment servers (a, b, c).
Fragment server a:
[14, 15, 7, 5, 11, 9]
Fragment server b:
[3, 4, 12, 2, 7, 5]
Fragment server c:
[0, 2, 11, 7, 12, 12]
Tally is 157
```
6. To stop a fragment servers, run:
```
#> stop 
```
If one fragment server has been stopped, all fragment servers need to be stopped before trying to start again.

## Notes:
- The fragment servers currently all use the same certificate for network communications.
- This code is currently for example purposes and is thus not performance optimised. 
- There can be errors where the number of votes is slightly wrong. Given the inconsistency of these errors, the scheduler is probably the issue. 
