#!/usr/bin/env python
#
# Test cases for tournament.py
# To support multiple tournaments I have made some modifications
# to this test file. I added an additional test step and modified
# later tests to create tournaments and register players to those
# tournaments.

from tournament import *


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testCreateDeleteTournament():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    createTournament("Fall Championship")
    createTournament("Winter Championship")
    c = countTournaments()
    if c != 2:
        raise ValueError(
            "After creating 2 tournaments, countTournaments should be 2.")
    deleteTournaments()
    c = countTournaments()
    if c != 0:
        raise ValueError(
            "After deleting, countTournaments should return zero.")
    print "6. Tournaments can be created and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    createTournament("Summer Showdown")
    tournaments = listTournaments()
    players = listPlayers()
    for (id, name) in players:
        for (t_id, t_name) in tournaments:
            addPlayerToTournamentRoster(t_id, id)
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings "
                         "even before they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 7:
        raise ValueError("Each playerStandings row should have seven columns.")
    [(id1, name1, t_id1, t_name1, wins1, matches1, winpercent1),
     (id2, name2, t_id2, t_name2, wins2, matches2, winpercent2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in "
                         "standings, even if they have no matches played.")
    print "7. Newly registered players appear in the standings with no matches."  # noqa


def testReportMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    createTournament("Winter Championship")
    tournaments = listTournaments()
    players = listPlayers()
    for (t_id, t_name) in tournaments:
        for (id, name) in players:
            addPlayerToTournamentRoster(t_id, id)
        standings = playerStandings()
        [id1, id2, id3, id4] = [row[0] for row in standings]
        reportMatch(t_id, id1, id2)
        reportMatch(t_id, id3, id4)
    standings = playerStandings()
    for (i, n, t_i, t_n, w, m, wp) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError(
                "Each match loser should have zero wins recorded.")
    print "8. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    createTournament("Open Invitational")
    createTournament("Tournament of Champions")
    tournaments = listTournaments()
    players = listPlayers()
    for (t_id, t_name) in tournaments:
        for (id, name) in players:
            addPlayerToTournamentRoster(t_id, id)
        standings = playerStandings(t_id)
        [id1, id2, id3, id4] = [row[0] for row in standings]
        reportMatch(t_id, id1, id2)
        reportMatch(t_id, id3, id4)
        pairings = swissPairings(t_id)
        if len(pairings) != 2:
            raise ValueError(
                "For four players, swissPairings should return two pairs.")
        [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
        correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
        actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
        if correct_pairs != actual_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "9. After one match, players with one win are paired."


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testCreateDeleteTournament()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
