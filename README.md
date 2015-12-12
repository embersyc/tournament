# Tournament
Tournament project for Udacity nanodegree

##Prerequistes:

You will need to install the vagrant virtual machine following the instructions here:
  https://www.udacity.com/wiki/ud197/install-vagrant

Fork the repository and place the files in your vagrant virtual machine. 

##Instructions

Once vagrant is running, From the vagrant command line run:

  psql -f tournament.sql

This sets up the database. Next to run the program type:

  python tournament_test.py
  
The output should look like:

1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Tournaments can be created and deleted.
7. Newly registered players appear in the standings with no matches.
8. After a match, players have updated standings.
9. After one match, players with one win are paired.
Success!  All tests pass!


