drop table if exists account, reh_base, room, rehearsal, equipment cascade;

CREATE TABLE Account (
    ID serial NOT NULL PRIMARY KEY,
    fio text NOT NULL,
    phone text,
    mail text,
	password text,
	type text NOT NULL
);

CREATE TABLE Reh_base (
    ID serial NOT NULL PRIMARY KEY,
    ownerID int NOT NULL REFERENCES Account(ID),
    name text NOT NULL,
    address text NOT NULL,
    phone text,
	mail text
);

CREATE TABLE Room (
    ID serial NOT NULL PRIMARY KEY,
    baseID int NOT NULL REFERENCES Reh_base(ID),
    name text NOT NULL,
	type text,
	area int,
    cost int
);

CREATE TABLE Equipment (
    ID serial NOT NULL PRIMARY KEY,
    roomID int NOT NULL REFERENCES Room(ID),
	type text NOT NULL,
	brand text,
    amount int NOT NULL
);

CREATE TABLE Rehearsal (
    ID serial NOT NULL PRIMARY KEY,
    musicianID int NOT NULL REFERENCES Account(ID),
	roomID int NOT NULL REFERENCES Room(ID),
	rehDate timestamp
);

drop user if exists musician, base_owner, app_admin;

create user musician with password 'muse';
grant select, insert, delete on rehearsal to musician;
grant all privileges on account to musician;
grant select on equipment, reh_base, room to musician;

create user base_owner with password 'belldom';
grant select, delete on rehearsal to base_owner;
grant all privileges on reh_base, equipment, room, account to base_owner;

create user app_admin with password 'linkinpark';
grant select, delete on rehearsal, reh_base, equipment, room to app_admin;
grant select on account to app_admin;