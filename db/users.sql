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
  `locked` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`uid`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_modulesByUser` AS select `mo`.`uid` AS `UID`,`mo`.`mid` AS `MID`,`mods`.`name` AS `NAME`,`mods`.`title` AS `TITLE` from (`portal_module2user` `mo` join `portal_modules` `mods`) where (`mods`.`mid` = `mo`.`mid`);

CREATE DEFINER=`root`@`localhost` FUNCTION `fn_getModuleName`(iUid int) RETURNS varchar(300) CHARSET utf8
BEGIN
RETURN (SELECT 
      GROUP_CONCAT(DISTINCT name SEPARATOR ', ')
FROM
    simple_library.portal_modules
WHERE
    mid  in (SELECT mid
FROM
    simple_library.portal_module2user
WHERE
    uid = iUid
));
END

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_AllUsers` AS
    SELECT 
        `portal_users`.`uid` AS `uid`,
        `portal_users`.`email` AS `email`,
        `portal_users`.`display` AS `display`,
        `portal_users`.`role` AS `role`,
        FN_GETMODULENAME(`portal_users`.`uid`) AS `modules`
    FROM
        `portal_users`

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_modulesByUser` AS
    SELECT 
        `mo`.`uid` AS `uid`,
        `mo`.`mid` AS `mid`,
        `mods`.`name` AS `name`,
        `mods`.`title` AS `title`
    FROM
        (`portal_module2user` `mo`
        JOIN `portal_modules` `mods`)
    WHERE
        (`mods`.`mid` = `mo`.`mid`)
        
CREATE DEFINER=`root`@`localhost` FUNCTION `fn_getBooksCountForSerie`(iSid int) RETURNS int(11)
RETURN (SELECT COUNT(*) FROM simple_library.lib_serie2book WHERE sid  = iSid)

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_AllSeries` AS
    SELECT 
        `lib_series`.`sid` AS `sid`,
        `lib_series`.`serie_name` AS `serie_name`,
        FN_GETBOOKSCOUNTFORSERIE(`lib_series`.`sid`) AS `books_count`
    FROM
        `lib_series`