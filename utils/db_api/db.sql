-- mafiabot.afisha definition
 -- Drop table
 -- DROP TABLE mafiabot.afisha;

CREATE TABLE mafiabot.afisha (id serial4 NOT NULL,
                                         "date" time NULL,
                                                     "location" text NULL,
                                                                     max_count int8 NULL,
                                                                                    decription text NULL,
                                                                                                    CONSTRAINT afisha_pkey PRIMARY KEY (id));

-- Permissions

ALTER TABLE mafiabot.afisha OWNER TO smartman;

GRANT ALL ON TABLE mafiabot.afisha TO smartman;

-- mafiabot."user" definition
 -- Drop table
 -- DROP TABLE mafiabot."user";

CREATE TABLE mafiabot."user" (id int4 NOT NULL GENERATED ALWAYS AS IDENTITY, -- mafiabot.afisha definition
 -- Drop table
 -- DROP TABLE mafiabot.afisha;

CREATE TABLE mafiabot.afisha (id serial4 NOT NULL,
                                         "date" time NULL,
                                                     "location" text NULL,
                                                                     max_count int8 NULL,
                                                                                    decription text NULL,
                                                                                                    CONSTRAINT afisha_pkey PRIMARY KEY (id));

-- Permissions

ALTER TABLE mafiabot.afisha OWNER TO smartman;

GRANT ALL ON TABLE mafiabot.afisha TO smartman;

-- mafiabot."user" definition
 -- Drop table
 -- DROP TABLE mafiabot."user";

CREATE TABLE mafiabot."user" (id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
                                                         telegram_id int4 NOT NULL,
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
                                                                                                                                                                                                                                                                 CONSTRAINT user_pkey PRIMARY KEY (id,
                                                                                                                                                                                                                                                                                                   telegram_id));

-- Permissions

ALTER TABLE mafiabot."user" OWNER TO smartman;

GRANT ALL ON TABLE mafiabot."user" TO smartman;

-- mafiabot.idushie definition
 -- Drop table
 -- DROP TABLE mafiabot.idushie;

CREATE TABLE mafiabot.idushie
    (id serial4 NOT NULL,
                id_users int8 NULL,
                              id_afisha int8 NULL,
                                             CONSTRAINT idushie_pkey PRIMARY KEY (id), CONSTRAINT idushie_id_afisha_fkey
     FOREIGN KEY (id_afisha) REFERENCES mafiabot.afisha(id) ON DELETE
     SET NULL ON UPDATE CASCADE);

-- Permissions

ALTER TABLE mafiabot.idushie OWNER TO smartman;

GRANT ALL ON TABLE mafiabot.idushie TO smartman;

telegram_id int4 NOT NULL,
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
                                                                                                                                                                                                        CONSTRAINT user_pkey PRIMARY KEY (id,
                                                                                                                                                                                                                                          telegram_id));

-- Permissions

ALTER TABLE mafiabot."user" OWNER TO smartman;

GRANT ALL ON TABLE mafiabot."user" TO smartman;

-- mafiabot.idushie definition
 -- Drop table
 -- DROP TABLE mafiabot.idushie;

CREATE TABLE mafiabot.idushie
    (id serial4 NOT NULL,
                id_users int8 NULL,
                              id_afisha int8 NULL,
                                             CONSTRAINT idushie_pkey PRIMARY KEY (id), CONSTRAINT idushie_id_afisha_fkey
     FOREIGN KEY (id_afisha) REFERENCES mafiabot.afisha(id) ON DELETE
     SET NULL ON UPDATE CASCADE);

-- Permissions

ALTER TABLE mafiabot.idushie OWNER TO smartman;

GRANT ALL ON TABLE mafiabot.idushie TO smartman;