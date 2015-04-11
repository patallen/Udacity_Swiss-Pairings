-- Table definitions for the tournament project.


-- Create table to hold players' unique ID and non-unique full name
create table players (
	id serial primary key,
	name text
);

-- Create table to hold maches and outcomes
-- Each column is a foreign key of players.id
create table matches (
	player1 integer references players(id),
	player2 integer references players(id),
	winner integer references players(id)
);

-- Create a view that retuns a table with the ID, 
-- name, number of matches won, and number of matches 
-- played for each regisered player ordered by number of wins.
create view rankings as
	select players.id
		, players.name
		, count(matches.winner) as wins
		, coalesce(m.matches, 0) as matches
	from players
	left join matches on players.id = matches.winner
	left join (
		select players.id, players.name, count(players.id) as matches 
		from players, matches 
		where players.id = matches.player1 or players.id = matches.player2 group by players.id
		)
		as m on m.id = players.id
        group by players.id, m.matches
	order by wins desc, matches desc;
