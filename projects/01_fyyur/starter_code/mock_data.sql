-- Artist

CREATE TABLE public.artist (
    id integer NOT NULL,
    name character varying NOT NULL,
    city character varying(120) NOT NULL,
    state character varying(120) NOT NULL,
    phone character varying(120),
    genres character varying[] NOT NULL,
    image_link character varying(500),
    facebook_link character varying(120),
    website character varying,
    seeking_venue boolean,
    seeking_description character varying(800)
);

INSERT INTO public.artist (id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) VALUES (4, 'Guns N Petals', 'San Francisco', 'CA', '326-123-5000', '{"Rock n Roll"}', 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80', 'https://www.facebook.com/GunsNPetals', 'https://www.gunsnpetalsband.com', true, 'Looking for shows to perform at in the San Francisco Bay Area!');
INSERT INTO public.artist (id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) VALUES (6, 'The Wild Sax Band', 'San Francisco', 'CA', '432-325-5432', '{Jazz,Classical}', 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80', NULL, NULL, false, NULL);
INSERT INTO public.artist (id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) VALUES (5, 'Matt Quevedo', 'New York', 'NY', '300-400-5000', '{Jazz}', 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80', 'https://www.facebook.com/mattquevedo923251523', NULL, false, NULL);
INSERT INTO public.artist (id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) VALUES (2, 'aajnkrglnçbng\t', 'gsrgsrg', 'VT', '123-456-0000', '{Classical,Country}', '', '', NULL, false, '');
INSERT INTO public.artist (id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) VALUES (1, 'Fake artist', 'Las Vegas', 'NE', '123-456-7890', '{Other}', 'https://cdn.pixabay.com/photo/2016/10/09/17/27/fake-1726362_1280.jpg', '', '', true, 'Mock Artist example');

-- Venue
CREATE TABLE IF NOT EXISTS public.venue
(
    id integer NOT NULL DEFAULT nextval('venue_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default" NOT NULL,
    address character varying(120) COLLATE pg_catalog."default" NOT NULL,
    city character varying(120) COLLATE pg_catalog."default" NOT NULL,
    state character varying(120) COLLATE pg_catalog."default" NOT NULL,
    phone character varying(120) COLLATE pg_catalog."default",
    genres character varying[] COLLATE pg_catalog."default" NOT NULL,
    website character varying COLLATE pg_catalog."default",
    image_link character varying(500) COLLATE pg_catalog."default",
    facebook_link character varying(120) COLLATE pg_catalog."default",
    seeking_talent boolean,
    seeking_description character varying(800) COLLATE pg_catalog."default",
    CONSTRAINT venue_pkey PRIMARY KEY (id)
)

INSERT INTO public.venue VALUES (2, 'The Dueling Pianos Bar', '335 Delancey Street', 'New York', 'NY', '914-003-1132', '{Classical,R&B,Hip-Hop}', 'https://www.theduelingpianos.com', 'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80', 'https://www.facebook.com/theduelingpianos', false, NULL);
INSERT INTO public.venue VALUES (3, 'Park Square Live Music & Coffee', '34 Whiskey Moore Ave', 'San Francisco', 'CA', '415-000-1234', '{"Rock n Roll",Jazz,Classical,Folk}', 'https://www.parksquarelivemusicandcoffee.com', 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80', 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee', false, NULL);
INSERT INTO public.venue VALUES (1, 'The Musical Hop', '1015 Folsom Street', 'San Francisco', 'CA', '123-123-1234', '{Classical,Folk,Jazz,Reggae}', 'https://www.themusicalhop.com', 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60', 'https://www.facebook.com/TheMusicalHop', true, 'We are on the lookout for a local artist to play every two weeks. Please call us.');
INSERT INTO public.venue VALUES (12, 'Fake Venue', 'Some fake addres, 000', 'Miami', 'FL', '987-654-3210', '{Blues,Classical,Country,Electronic,Folk,Funk,Hipop,HeavyMetal,Instrumental,Jazz}', '', 'https://cdn.pixabay.com/photo/2015/06/30/18/36/st-826688_1280.jpg', '', false, '');

-- shows

CREATE TABLE IF NOT EXISTS public.shows
(
    id integer NOT NULL DEFAULT nextval('shows_id_seq'::regclass),
    start_time timestamp without time zone NOT NULL,
    artist_id integer,
    venue_id integer,
    CONSTRAINT shows_pkey PRIMARY KEY (id),
    CONSTRAINT shows_artist_id_fkey FOREIGN KEY (artist_id)
        REFERENCES public.artist (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT shows_venue_id_fkey FOREIGN KEY (venue_id)
        REFERENCES public.venue (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

INSERT INTO public.shows VALUES (1, '2019-05-21 21:30:00', 4, 1);
INSERT INTO public.shows VALUES (2, '2035-04-01 20:00:00', 6, 3);
INSERT INTO public.shows VALUES (3, '2035-04-08 20:00:00', 6, 3);
INSERT INTO public.shows VALUES (4, '2035-04-15 20:00:00', 6, 3);
INSERT INTO public.shows VALUES (5, '2019-06-15 23:00:00', 5, 3);
INSERT INTO public.shows VALUES (6, '2022-10-18 13:04:30', 1, NULL);
INSERT INTO public.shows VALUES (7, '2022-10-22 21:13:05', 1, 12);