-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS mafiabot.afisha
(
    id  int8 NOT NULL,
    location text,
    max_count bigint,
    decription text,
    name text,
    date timestamp without time zone,
    photoid text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS mafiabot.idushie
(
    id  int8 NOT NULL,
    id_users  int8 NOT NULL,
    id_afisha  int8 NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS mafiabot."user"
(
    id  int8 NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    telegram_id  int8,
    telegram_nickname  varchar varying,
    fi_tg  varchar varying,
    fi_reg  varchar varying,
    city  varchar varying,
    nickname_mafia  varchar varying,
    proffesion  varchar varying,
    dohod  varchar varying,
    phone_number  varchar varying,
    photo_id  varchar varying,
    age  int8,
    date date,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS mafiabot.idushie
    ADD FOREIGN KEY (id_afisha)
    REFERENCES mafiabot.afisha (id)
    NOT VALID;


ALTER TABLE IF EXISTS mafiabot.idushie
    ADD FOREIGN KEY (id_users)
    REFERENCES mafiabot."user" (telegram_id)
    NOT VALID;

END;

-- mafiabot.afisha definition
-- Drop table
-- DROP TABLE mafiabot.afisha;

CREATE TABLE mafiabot.afisha (id serial4 NOT NULL,
"location" text NULL,
max_count int8 NULL,
decription text NULL,
"name" text NULL,
"date" timestamp NULL,
photoid text NULL,
CONSTRAINT afisha_pkey PRIMARY KEY (id));

-- Permissions

ALTER TABLE mafiabot.afisha OWNER TO smartman;

GRANT ALL ON TABLE mafiabot.afisha TO smartman;

-- mafiabot."user" definition
-- Drop table
-- DROP TABLE mafiabot."user";

CREATE TABLE mafiabot."user" (id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
telegram_id int4 NULL,
telegram_nickname varchar NULL,
fi_tg varchar NULL,
fi_reg varchar NULL,
city varchar NULL,
nickname_mafia varchar NULL,
proffesion varchar NULL,
dohod varchar NULL,
phone_number varchar NULL,
photo_id varchar NULL,
age int4 NULL,
"date" date NULL,
CONSTRAINT user_pk PRIMARY KEY (id));

-- Permissions

ALTER TABLE mafiabot."user" OWNER TO smartman;

GRANT ALL ON TABLE mafiabot."user" TO smartman;

-- mafiabot.idushie definition
-- Drop table
-- DROP TABLE mafiabot.idushie;

CREATE TABLE mafiabot.idushie
(id serial4 NOT NULL,
id_users int4 NULL,
id_afisha int4 NULL,
CONSTRAINT idushie_pkey PRIMARY KEY (id), CONSTRAINT idushie_fk
FOREIGN KEY (id) REFERENCES mafiabot."user"(id) ON DELETE
SET NULL,
CONSTRAINT idushie_id_afisha_fkey
FOREIGN KEY (id_afisha) REFERENCES mafiabot.afisha(id) ON DELETE
SET NULL ON UPDATE CASCADE);


CREATE INDEX idushie_id_idx ON mafiabot.idushie USING btree (id, id_users, id_afisha);

-- Permissions

ALTER TABLE mafiabot.idushie OWNER TO smartman;

GRANT ALL ON TABLE mafiabot.idushie TO smartman;