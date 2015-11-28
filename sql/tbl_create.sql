CREATE TABLE User (
	username varchar(20) PRIMARY KEY,
	password varchar(40)
);

CREATE TABLE BlogEntry (
	entryid int PRIMARY KEY AUTO_INCREMENT,
	entrydate date,
	content varchar(1000)
);
