CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

/*
CREATE TABLE public.teams (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.countries (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) UNIQUE NOT NULL,
	geom            GEOMETRY,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.players (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
	age             INT NOT NULL,
	team_id         uuid,
	country_id      uuid NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE players
    ADD CONSTRAINT players_countries_id_fk
        FOREIGN KEY (country_id) REFERENCES countries
            ON DELETE CASCADE;

ALTER TABLE players
    ADD CONSTRAINT players_teams_id_fk
        FOREIGN KEY (team_id) REFERENCES teams
            ON DELETE SET NULL;
*/


CREATE TABLE public.event (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	event          VARCHAR(250) NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.atlethe (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
	sex             VARCHAR(250) NOT NULL,
	age            	VARCHAR(250) NOT NULL,
	height          VARCHAR(250) NOT NULL,
	weight          VARCHAR(250) NOT NULL,
	team            VARCHAR(250) NOT NULL,
	noc        	    VARCHAR(250) NOT NULL,
	games           VARCHAR(250) NOT NULL,
	year            VARCHAR(250) NOT NULL,
	season          VARCHAR(250) NOT NULL,
	city            VARCHAR(250) NOT NULL,
	lat         	VARCHAR(250) NOT NULL,
	lon             VARCHAR(250) NOT NULL,
	sport           VARCHAR(250) NOT NULL,
	event           VARCHAR(250) NOT NULL,
	medal           VARCHAR(250) NOT NULL,
	geom            GEOMETRY,
	event_id 		uuid,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE atlethe
    ADD CONSTRAINT atlethe_event_id_fk
        FOREIGN KEY (event_id) REFERENCES event
            ON DELETE SET NULL;
