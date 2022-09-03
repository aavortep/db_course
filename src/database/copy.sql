truncate rehearsal, equipment, room, reh_base, account cascade;
COPY account FROM 'C:/Anya/Prog/Course_works/db_course/src/database/accs.txt' WITH (DELIMITER '|');
COPY reh_base FROM 'C:/Anya/Prog/Course_works/db_course/src/database/bases.txt' WITH (DELIMITER '|');
COPY room FROM 'C:/Anya/Prog/Course_works/db_course/src/database/rooms.txt' WITH (DELIMITER '|');
COPY equipment FROM 'C:/Anya/Prog/Course_works/db_course/src/database/equip.txt' WITH (DELIMITER '|');
COPY rehearsal FROM 'C:/Anya/Prog/Course_works/db_course/src/database/rehs.txt' WITH (DELIMITER '|');