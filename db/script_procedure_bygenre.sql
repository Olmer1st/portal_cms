set @iGid = 24;
set @sLang = 'ru';
set @iDel = 1;

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
        
SET @str_part = CONCAT(@str_start , @iGid,')');
SET @lng_str = ' and LANG =\'ru\'';
SET @del_str = ' and DEL is NULL';

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
