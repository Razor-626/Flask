CREATE TABLE IF NOT EXISTS mainmenu(
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts(
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
description text NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS users(
id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
password text NOT NULL
)