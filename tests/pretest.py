
reftable = """
CREATE TABLE `by0001` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `fld1` char(10) DEFAULT NULL,
  `fld2` smallint(6) DEFAULT NULL,
  `fld4` mediumint(9) DEFAULT NULL,
  `fld5` int(11) DEFAULT NULL,
  `fld6` bigint(20) DEFAULT NULL,
  `fld7` float DEFAULT NULL,
  `fld8` double DEFAULT NULL,
  `fld9` double DEFAULT NULL,
  `fld10` double DEFAULT NULL,
  `fld11` decimal(10,2) DEFAULT NULL,
  `fld12` bit(1) DEFAULT NULL,
  `fld13` double DEFAULT NULL,
  `fld14` tinyint(1) DEFAULT NULL,
  `fld15` text DEFAULT NULL,
  `fld16` blob DEFAULT NULL,
  `fld17` enum('123','234') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
"""

usertable = """
CREATE TABLE `users_1111` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) DEFAULT NULL,
  `uid` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `owner_id` int(11) unsigned DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
"""

userdata = [
    "insert into users_1111 (first_name, uid, email, owner_id) \
                values ('hhhh', '13221312-123123123-123123', 'food@example.com', 1);",
    "insert into users_1111 (first_name, uid, email, owner_id) \
                values ('bbbb', '13221312-123123123-343434', 'food@example.com', 1);"
]


garbagetable = """
CREATE TABLE `garbage_1111` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `scoops` int(11) DEFAULT NULL,
  `boops` varchar(50) DEFAULT NULL,
  `user_id` int(11) default null,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=utf8mb3;
"""

garbagedata = [
    "insert into garbage_1111 (scoops, boops, user_id) \
                values (44, 'jjjkkkkkkkkkkkk', 1);",
    "insert into garbage_1111 (scoops, boops, user_id) \
                values (88, 'dfsdfdfsdfsdfsdf', 1);",
]

teardown = [
    "drop table if exists garbage_1111;",
    "drop table if exists users_1111;"
]
