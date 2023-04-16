create table if not exists Users (
	user_id int primary key not null,
	user_age int not null,
	user_gender varchar(10) not null,
	user_city varchar(50) not null
);

create table if not exists FavoriteClients (
	client_id int primary key not null,
	client_name varchar(20) not null,
	client_surname varchar(50) not null,
	client_link text not null,
	client_photos text
);

create table "Users/Client" (
	user_id int references users(user_id) not null,
	favoriteclient_id int references FavoriteClients(client_id) not null,
	primary key(user_id, favoriteclient_id)
);

create table "Users/Propose" (
	user_id int references users(user_id) not null,
	prop_client_id int not null,
	primary key(user_id, prop_client_id)
);
