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



CREATE DEFINER=`root`@`localhost` FUNCTION `fn_getModuleName`(iUid int) RETURNS varchar(300) CHARSET utf8
RETURN (SELECT  GROUP_CONCAT(DISTINCT name SEPARATOR ', ') FROM simple_library.portal_modules WHERE mid  in (SELECT mid FROM simple_library.portal_module2user WHERE uid = iUid));


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

CREATE DEFINER=`root`@`localhost` FUNCTION `fn_getBooksCountForGenre`(iGid int) RETURNS int(11)
RETURN (SELECT COUNT(*) FROM simple_library.lib_genre2book WHERE gid  = iGid)
       
        
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_AllGenreGroups` AS
    SELECT 
        `lib_genres`.`gid` AS `gid`,
        `lib_genres`.`code` AS `code`,
        `lib_genres`.`gdesc` AS `gdesc`,
        `lib_genres`.`edesc` AS `edesc`
    FROM
        `lib_genres`
    WHERE
        `lib_genres`.`gid` IN (SELECT DISTINCT
                `lib_genre2group`.`gidm`
            FROM
                `lib_genre2group`)
    ORDER BY `lib_genres`.`gdesc`
    
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_AllGenres` AS
    SELECT 
        `lib_genres`.`gid` AS `gid`,
        `lib_genres`.`code` AS `code`,
        `lib_genres`.`gdesc` AS `gdesc`,
        `lib_genres`.`edesc` AS `edesc`,
        FN_GETBOOKSCOUNTFORGENRE(`lib_genres`.`gid`) AS `books_count`
    FROM
        `lib_genres`
    WHERE
        (NOT (`lib_genres`.`gid` IN (SELECT DISTINCT
                `lib_genre2group`.`gidm`
            FROM
                `lib_genre2group`)))
    ORDER BY `lib_genres`.`gdesc`
    
    
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_genreByGenreGroup` AS
    SELECT 
        `gs`.`gid` AS `gid`,
        `gg`.`gidm` AS `gidm`,
        `gs`.`code` AS `code`,
        `gs`.`gdesc` AS `gdesc`,
        `gs`.`edesc` AS `edesc`,
        FN_GETBOOKSCOUNTFORGENRE(`gs`.`gid`) AS `books_count`
    FROM
        (`lib_genres` `gs`
        JOIN `lib_genre2group` `gg`)
    WHERE
        ((NOT (`gs`.`gid` IN (SELECT DISTINCT
                `lib_genre2group`.`gidm`
            FROM
                `lib_genre2group`)))
            AND (`gg`.`gid` = `gs`.`gid`))
    ORDER BY `gs`.`gdesc`
    
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_booksByGenre` AS
    SELECT 
        `ge`.`gid` AS `GID`,
        `au`.`aid` AS `AID`,
        `books`.`BID` AS `BID`,
        `books`.`TITLE` AS `TITLE`,
        FN_GETGENRENAMES(`books`.`BID`) AS `GENRE`,
        `books`.`SERIES` AS `SERIE_NAME`,
        `books`.`SERNO` AS `SERIE_NUMBER`,
        `books`.`FILE` AS `FILE`,
        `books`.`EXT` AS `EXT`,
        `books`.`DEL` AS `DEL`,
        `books`.`LANG` AS `LANG`,
        `books`.`SIZE` AS `SIZE`,
        `books`.`DATE` AS `DATE`,
        `books`.`LIBRATE` AS `LIBRATE`,
        `books`.`KEYWORDS` AS `KEYWORDS`,
        `books`.`PATH` AS `PATH`
    FROM
        ((`lib_genre2book` `ge`
        JOIN `lib_author2book` `au`)
        JOIN `lib_books` `books`)
    WHERE
        ((`au`.`bid` = `books`.`BID`)
            AND (`ge`.`bid` = `books`.`BID`))
    ORDER BY `books`.`SERNO`
    
    CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_AllLanguages` AS
    SELECT DISTINCT
        `lib_books`.`LANG` AS `LANG`
    FROM
        `lib_books`
        
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getBooksByGenre`(IN iGid BIGINT, IN sLang varchar(5), IN iDel INT)
BEGIN
SET @str_start = 'create temporary table tmp_books (PRIMARY KEY bid_key(BID)) select 
        `books`.`BID` AS `BID`,
        `books`.`TITLE` AS `TITLE`,
        FN_GETGENRENAMES(`books`.`BID`) AS `GENRE`,
        `books`.`SERIES` AS `SERIE_NAME`,
        `books`.`SERNO` AS `SERIE_NUMBER`,
        `books`.`FILE` AS `FILE`,
        `books`.`EXT` AS `EXT`,
        `books`.`DEL` AS `DEL`,
        `books`.`LANG` AS `LANG`,
        `books`.`SIZE` AS `SIZE`,
        `books`.`DATE` AS `DATE`,
        `books`.`LIBRATE` AS `LIBRATE`,
        `books`.`KEYWORDS` AS `KEYWORDS`,
        `books`.`PATH` AS `PATH` from lib_books books where bid  in (select bid from lib_genre2book where gid =';
        
SET @str_part = CONCAT(@str_start ,iGid,')');
SET @lng_str = '';
SET @del_str = '';
IF not sLang is NULL and LENGTH(sLang)>0 THEN
	SET @lng_str = CONCAT(' and LANG =\'', sLang,'\'');
END IF;
IF iDel>0 THEN
	SET @del_str = ' and DEL is NULL';
END IF;
SET @str_sql = CONCAT(@str_part,@lng_str,@del_str, ' ORDER BY SERNO');

PREPARE stmt FROM @str_sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

select ab.AID, bo.* from lib_author2book ab, tmp_books bo
where ab.bid = bo.bid order by SERIE_NUMBER;

select AID, FULLNAME  
from lib_authors where AID in (select distinct aid from  lib_author2book where bid in (select bid from  tmp_books))
order by FULLNAME;

drop temporary table if exists tmp_books;
END