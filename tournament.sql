-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
	player_id SERIAL,
	name TEXT NOT NULL,
	PRIMARY KEY (player_id)
);

CREATE TABLE tournaments (
	tournament_id SERIAL,
	name TEXT NOT NULL,
	PRIMARY KEY (tournament_id)
);

-- Intentionally allowing loser to be NULL below to support BYE rounds. 
CREATE TABLE matches (
	match_id SERIAL,
	tournament INTEGER REFERENCES tournaments(tournament_id) NOT NULL,
	winner INTEGER REFERENCES players(player_id) NOT NULL,
	loser INTEGER REFERENCES players(player_id),
	PRIMARY KEY (match_id)
);

CREATE TABLE tournament_players (
	tournament INTEGER REFERENCES tournaments(tournament_id) NOT NULL,
	player INTEGER REFERENCES players(player_id) NOT NULL
);

CREATE VIEW tournament_rosters AS
	SELECT 
		players.player_id, 
		players.name AS player_name, 
		tournament_players.tournament AS tournament_id,
		tournaments.name AS tournament_name
	FROM players JOIN tournament_players 
	ON players.player_id = tournament_players.player
	JOIN tournaments
	ON tournaments.tournament_id = tournament_players.tournament
	ORDER BY tournament_players.tournament;

CREATE VIEW wincounts AS
	SELECT 
		tournament_rosters.player_id, 
		tournament_rosters.player_name, 
		tournament_rosters.tournament_id, 
		tournament_rosters.tournament_name,
		count(matches.winner) as wins
	FROM tournament_rosters LEFT JOIN matches
	ON tournament_rosters.player_id = matches.winner 
	AND tournament_rosters.tournament_id = matches.tournament
	GROUP BY 
		tournament_rosters.player_id, 
		tournament_rosters.player_name, 
		tournament_rosters.tournament_id,
		tournament_rosters.tournament_name
	ORDER BY tournament_rosters.tournament_id, wins DESC;
	
CREATE VIEW matchcounts AS
	SELECT 
		tournament_rosters.player_id, 
		tournament_rosters.player_name, 
		tournament_rosters.tournament_id,
		tournament_rosters.tournament_name,
		count(matches.winner+matches.loser) as matches
	FROM tournament_rosters LEFT JOIN matches
	ON (tournament_rosters.player_id = matches.winner 
	OR tournament_rosters.player_id = matches.loser)
	AND tournament_rosters.tournament_id = matches.tournament
	GROUP BY 
		tournament_rosters.player_id, 
		tournament_rosters.player_name, 
		tournament_rosters.tournament_id,
		tournament_rosters.tournament_name
	ORDER BY tournament_rosters.tournament_id, matches DESC;
	
CREATE VIEW standings AS
	SELECT 
		matchcounts.player_id, 
		matchcounts.player_name, 
		matchcounts.tournament_id,
		matchcounts.tournament_name,
		wincounts.wins, 
		matchcounts.matches,
		CASE WHEN (matchcounts.matches > 0) THEN 
		CAST(wincounts.wins as REAL) / CAST(matchcounts.matches as REAL)
		ELSE 0.00 END as win_percentage
	FROM wincounts RIGHT JOIN matchcounts
	ON wincounts.player_id = matchcounts.player_id 
	AND wincounts.tournament_id = matchcounts.tournament_id
	ORDER BY matchcounts.tournament_id, win_percentage DESC, matchcounts.matches desc;