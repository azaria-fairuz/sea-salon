drop schema if exists "user" cascade;
drop schema if exists "salon" cascade;

create schema "user";

create table if not exists "user".roles (
	id varchar(4) primary key,
	name varchar(20) unique not null
);

create table if not exists "user".data (
	id varchar(4),
	name varchar(50) not null,
	email varchar(30) unique not null,
	phone numeric(10) unique not null,
	password varchar(20) not null,
	role varchar(20) not null,
	
	primary key(id),
	constraint user_role foreign key(role) references "user".roles(name)
);

create schema "salon";

create table if not exists "salon".branches (
	id varchar(4),
	name varchar(20) unique not null,
	address varchar(256) not null,
	open time not null,
	close time not null,
	
	primary key(id)
);

create table if not exists "salon".services (
	id varchar(12),
	service varchar(128) not null,
	branch varchar(20) not null,
	
	primary key(id),
	constraint salon_branch foreign key(branch) references "salon".branches(name)
);

create table if not exists "salon".reservations (
	id varchar(12),
	user_id varchar(4) not null, 
	phone numeric(10) not null, 
	service_id varchar(12) not null, 
	date timestamp unique not null, 
	status char(1) not null,
	
	primary key(id),
	constraint username_id foreign key(user_id) references "user".data(id),
	constraint user_phone foreign key(phone) references "user".data(phone),
	constraint salon_service foreign key(service_id) references "salon".services(id)
);

create table if not exists "user".reviews (
	id varchar(12), 
	user_id varchar(4) not null, 
	service_id varchar(12) not null,
	branch varchar(20) not null,
	rating numeric(1) not null, 
	notes varchar(256) not null,
	
	primary key(id),
	constraint username_id foreign key(user_id) references "user".data(id),
	constraint salon_service foreign key(service_id) references "salon".services(id),
	constraint salon_branch foreign key(branch) references "salon".branches(name)
);
