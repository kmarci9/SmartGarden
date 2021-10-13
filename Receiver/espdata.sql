-- Table: public.espdata

--DROP TABLE public.espdata;

CREATE TABLE public.espdata
(
 id serial primary key,
 created timestamp not null,
 soil real,
 temperature real
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.espdata
  OWNER TO pi;