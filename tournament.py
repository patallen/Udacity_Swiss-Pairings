#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players")
    count = c.fetchone()
    db.close()
    return int(count[0])


def registerPlayer(name):
    """Adds a player to the tournament database."""
    db = connect()
    c = db.cursor()
    c.execute("insert into players (name) values (%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """
    Returns a list of the players and their win records, sorted by wins.
    Returns a list of tuples, each of which contains (id, name, wins, matches):
    """
    db = connect()
    c = db.cursor()
    c.execute("select * from rankings;")
    result = c.fetchall()
    db.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players."""
    db = connect()
    c = db.cursor()
    c.execute("insert into matches values (%s, %s, %s)",
              (winner, loser, winner))
    db.commit()
    db.close()


def swissPairings():
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
    standings = playerStandings()
    count = 0
    pairs = []

    # for every other row in standings, it's ID and name
    # is paired with the ID and name of the row below it
    while count < len(standings):
        player1id = standings[count][0]
        player1name = standings[count][1]
        player2id = standings[count + 1][0]
        player2name = standings[count + 1][1]
        pairs.append((player1id, player1name, player2id, player2name))
        count = count + 2

    return pairs
