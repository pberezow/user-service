-- Table: users
--DROP TABLE users;
CREATE TABLE users
(
  id serial,
  password character varying(128) NOT NULL,
  last_login timestamp with time zone DEFAULT NULL,
  username character varying(150) NOT NULL,
  first_name character varying(30) NOT NULL,
  last_name character varying(150) NOT NULL,
  email character varying(254) NOT NULL,
  is_active boolean NOT NULL,
  date_joined timestamp with time zone NOT NULL DEFAULT NOW(),
  licence_id integer NOT NULL,
  is_admin boolean NOT NULL,
  phone_number character varying(12) NOT NULL,
  address character varying(100) NOT NULL,
  "position" character varying(30) NOT NULL,
  CONSTRAINT users_pkey PRIMARY KEY (id),
  CONSTRAINT users_username_key UNIQUE (username)
);


-- Table: groups
--DROP TABLE groups;
CREATE TABLE groups
(
  id serial,
  licence_id integer NOT NULL,
  name character varying(30) NOT NULL,
  CONSTRAINT groups_pkey PRIMARY KEY (id),
  CONSTRAINT groups_licence_id_name UNIQUE (licence_id, name)
);


-- Table: users_groups
--DROP TABLE users_groups;
CREATE TABLE users_groups
(
  user_id integer NOT NULL,
  group_id integer NOT NULL,
  CONSTRAINT users_groups_pkey PRIMARY KEY (user_id, group_id),
  CONSTRAINT users_groups_group_id_fk_groups_id FOREIGN KEY (group_id)
      REFERENCES groups (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT users_groups_user_id_fk_users_id FOREIGN KEY (user_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
);


-- Table: reset_password_token
--DROP TABLE reset_password_token;
CREATE TABLE reset_password_token
(
  user_id integer NOT NULL,
  token character varying(600) NOT NULL,
  CONSTRAINT reset_password_token_pkey PRIMARY KEY (user_id),
  CONSTRAINT users_id_fk_user_id FOREIGN KEY (user_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT reset_password_token_token UNIQUE (token)
);
