drop table predicts;
create table predicts
(id serial primary key,
 rp5 numeric not null,
 GISMETEO numeric not null,
 MailRu numeric not null,
 curr numeric
);

INSERT INTO predicts (rp5, GISMETEO, MailRu, curr) VALUES
-- День 1: все верно
(22, 22, 22, 22),
-- День 2: все совпадают, но ошиблись
(18, 18, 18, 20),
-- День 3: RP5 ошибся
(25, 23, 23, 23),
-- День 4: MailRu точный
(21, 21, 19, 19),
-- День 5: все разные, но GISMETEO точный
(17, 16, 15, 16),
-- День 6: все ошиблись
(28, 27, 28, 25),
-- День 7: совпали RP5 и GISMETEO
(24, 24, 22, 24),
-- День 8: все разные, все ошиблись
(19, 20, 18, 21),
-- День 9: точный прогноз
(26, 26, 26, 26),
-- День 10: RP5 сильно ошибся
(30, 23, 23, 23),
-- День 11: совпали GISMETEO и MailRu
(21, 20, 20, 20),
-- День 12: все близки, но ошиблись
(16, 17, 17, 19),
-- День 13: RP5 единственный верный
(22, 20, 21, 22),
-- День 14: все одинаковые и верные
(18, 18, 18, 18),
-- День 15: все ошиблись по-разному
(27, 25, 26, 24),
-- День 16: MailRu единственный верный
(23, 22, 21, 21),
-- День 17: небольшие расхождения
(19, 20, 20, 20),
-- День 18: RP5 сильно завысил
(29, 24, 25, 24),
-- День 19: все одинаковые, но ошиблись
(22, 22, 22, 20),
-- День 20: идеальный прогноз
(25, 25, 25, 25),
-- День 21: RP5 занизил
(18, 22, 22, 22),
-- День 22: все разные, все неверные
(17, 18, 19, 16),
-- День 23: GISMETEO единственный верный
(24, 23, 25, 23),
-- День 24: совпали RP5 и MailRu
(20, 19, 20, 19),
-- День 25: все ошиблись одинаково
(28, 28, 28, 26),
-- День 26: нормальный разброс
(21, 22, 20, 21),
-- День 27: RP5 точно угадал
(19, 18, 17, 19),
-- День 28: все близко, но мимо
(23, 24, 24, 22),
-- День 29: два верных прогноза
(24, 24, 23, 24),
-- День 30: полный провал прогнозов
(30, 28, 29, 25);

CREATE or replace FUNCTION rp5acc() RETURNS numeric AS $$
begin
    return (select round((sum(matching)::numeric/sum(total)::numeric), 2) as res from
			(select case
		   when rp5 = curr then 1
		   else 0
		   end as matching, 1 as total from predicts));
end;
$$ LANGUAGE plpgsql;

CREATE or replace FUNCTION GISMETEOacc() RETURNS numeric AS $$
begin
    return (select round((sum(matching)::numeric/sum(total)::numeric), 2) as res from
			(select case
		   when GISMETEO = curr then 1
		   else 0
		   end as matching, 1 as total from predicts));
end;
$$ LANGUAGE plpgsql;

CREATE or replace FUNCTION MailRuacc() RETURNS numeric AS $$
begin
    return (select round((sum(matching)::numeric/sum(total)::numeric), 2) as res from
			(select case
		   when MailRu = curr then 1
		   else 0
		   end as matching, 1 as total from predicts));
end;
$$ LANGUAGE plpgsql;

select rp5acc(), GISMETEOacc(), MailRuacc()
select * from predicts