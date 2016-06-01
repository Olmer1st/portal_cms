CREATE TABLE `portal_module2user` (
  `uid` int(11) unsigned NOT NULL,
  `mid` int(10) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `portal_modules` (
  `mid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`mid`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

CREATE TABLE `portal_users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `display` varchar(200) NOT NULL,
  `password` varchar(300) NOT NULL,
  `role` varchar(20) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_modulesByUser` AS select `mo`.`uid` AS `UID`,`mo`.`mid` AS `MID`,`mods`.`name` AS `NAME`,`mods`.`title` AS `TITLE` from (`portal_module2user` `mo` join `portal_modules` `mods`) where (`mods`.`mid` = `mo`.`mid`);
