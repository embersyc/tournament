#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tournament_players")
    cursor.execute("DELETE FROM players")
    db.commit()
    db.close()


def deleteTournaments():
    """Remove all the tournament records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tournaments")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT count(*) as num FROM players")
    count = cursor.fetchone()[0]
    db.close()
    return count


def countTournaments():
    """Returns the number of tournaments currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT count(*) as num FROM tournaments")
    count = cursor.fetchone()[0]
    db.close()
    return count


def createTournament(name):
    """Adds a tournament to the database.

    Args:
      name: the tournament's name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tournaments (name) VALUES (%s)",
                   (bleach.clean(name), ))
    db.commit()
    db.close()


def listTournaments():
    """Returns a list of tournaments sorted by id.

    Returns:
      A list of tuples, each of which contains (id, name):
        id: the tournament's unique id (assigned by the database)
        name: the tournament's name (as registered)
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tournaments")
    tournaments = cursor.fetchall()
    db.close()
    return tournaments


def listPlayers():
    """Returns a list of players sorted by id.

    Returns:
      A list of tuples, each of which contains (id, name):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    db.close()
    return players


def registerPlayer(name):
    """Adds a player to the players database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s)",
                   (bleach.clean(name), ))
    db.commit()
    db.close()


def addPlayerToTournamentRoster(tournament_id, player_id):
    """Adds a previously registered player to a tournament's roster.

    Args:
      tournament_id: the id of the tournament the player should be added to
      played_id: the id of the player to add.

    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("""INSERT INTO tournament_players (tournament, player)
                   VALUES (%s, %s)""", (tournament_id, player_id))
    db.commit()
    db.close()


def playerStandings(tournament_id=-1):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains:
        player_id: the player's unique id (assigned by the database)
        player_name: the player's full name (as registered)
        tournament_id: the tournament's unqiue id (assigned by the database)
        tournament_name: the tournament name (assigned by the database)
        wins: the number of matches the player has won in this tournament
        matches: the number of matches the player has played in this tournament
        win_percentage: The overall win percentage the player has
    """
    db = connect()
    cursor = db.cursor()
    if tournament_id == -1:
        cursor.execute("SELECT * FROM standings")
    else:
        cursor.execute("SELECT * FROM standings WHERE tournament_id = %s",
                       (tournament_id, ))
    standings = cursor.fetchall()
    db.close()
    return standings


def reportMatch(tournament, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      tournament: the id of the tournament the match is for
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("""INSERT INTO matches (tournament, winner, loser)
                   VALUES (%s, %s, %s)""", (tournament, winner, loser))
    db.commit()
    db.close()


def swissPairings(tournament_id):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings(tournament_id)
    pairings = []
    for i in range(0, len(standings), 2):
        id1 = standings[i][0]
        name1 = standings[i][1]
        i += 1
        id2 = standings[i][0]
        name2 = standings[i][1]
        pairings.append((id1, name1, id2, name2))
    return pairings
