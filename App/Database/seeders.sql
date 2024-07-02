-- create extentions needed
create extension if not exists pgcrypto;

-- roles
truncate "user".roles cascade;
insert into "user".roles(id, name) values ('admn', 'Admin');
insert into "user".roles(id, name) values ('cstr', 'Customer');

-- user
truncate "user".data cascade;
insert into "user".data(id, name, email, phone, password, role) 
values ('admn0000', 'Thomas N', 'thomas.n@compfest.id', '08123456789', crypt(' Admin123', gen_salt('md5')), 'Admin');
insert into "user".data(id, name, email, phone, password, role) 
values ('cstr0000', 'Jonathan Baker', 'jonathan.baker@mail.id', '081234567890', crypt(' Customer123', gen_salt('md5')), 'Customer');

-- branches
truncate "salon".branches cascade;
insert into "salon".branches(id, name, address, open, close, time_zone) 
values ('jkrt0000', 'SEA SALON: JAKARTA', '123 Imaginary Street, Dreamland, Fictitious County, ABC123', '09:00:00', '21:00:00', 'WIB');
insert into "salon".branches(id, name, address, open, close, time_zone) 
values ('srby0001', 'SEA SALON: SURABAYA', '456 Fantasy Avenue, Wonderland, Make-Believe City, XY987', '07:00:00', '19:00:00', 'WIB');

-- services
truncate "salon".services cascade;
insert into "salon".services(id, service, branches) 
values ('jkrt00000001', 'Haircuts & Styling', 'jkrt0000');
insert into "salon".services(id, service, branches) 
values ('jkrt00000002', ' Manicure & Pedicure', 'jkrt0000');
insert into "salon".services(id, service, branches) 
values ('jkrt00000003', 'Facial Treatments', 'jkrt0000');
insert into "salon".services(id, service, branches) 
values ('srby00010001', 'Haircuts & Styling', 'srby0001');
insert into "salon".services(id, service, branches) 
values ('srby00010001', 'Facial Treatments', 'srby0001');

-- reviews
truncate "user".reviews cascade;
insert into "salon".reviews(id, user_id, service_id, branch_id, rating, notes) 
values ('202407020001', 'cstr0000', 'jkrt00000001', 'jkrt0000', 5, 'Highly recommend SEA Salon for anyone looking for top-notch hair and beauty treatments. A must-visit!');
insert into "salon".reviews(id, user_id, service_id, branch_id, rating, notes) 
values ('202407020002', 'cstr0000', 'jkrt00000002', 'jkrt0000', 4, 'Fantastic manicure and pedicure at SEA Salon. The staff was friendly, and my nails look fabulous!');
insert into "salon".reviews(id, user_id, service_id, branch_id, rating, notes) 
values ('202407020003', 'cstr0000', 'jkrt00000003', 'jkrt0000', 5, 'Had a rejuvenating facial at SEA Salon. My skin feels amazing—definitely coming back!');

