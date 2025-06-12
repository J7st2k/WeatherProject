create table predicts
(id serial primary key,
 rp5 numeric not null,
 GISMETEO numeric not null,
 MailRu numeric not null,
 rp5curr numeric not null,
 gismeteocurr numeric not null,
 mailrucurr numeric not null
);

CREATE or replace FUNCTION rp5acc() RETURNS numeric AS $$
begin
    return (select round((sum(matching)::numeric/sum(total)::numeric), 2) as res from
			(select case
		   when rp5 = rp5curr then 1
		   else 0
		   end as matching, 1 as total from predicts));
end;
$$ LANGUAGE plpgsql;

CREATE or replace FUNCTION GISMETEOacc() RETURNS numeric AS $$
begin
    return (select round((sum(matching)::numeric/sum(total)::numeric), 2) as res from
			(select case
		   when GISMETEO = gismeteocurr then 1
		   else 0
		   end as matching, 1 as total from predicts));
end;
$$ LANGUAGE plpgsql;

CREATE or replace FUNCTION MailRuacc() RETURNS numeric AS $$
begin
    return (select round((sum(matching)::numeric/sum(total)::numeric), 2) as res from
			(select case
		   when MailRu = mailrucurr then 1
		   else 0
		   end as matching, 1 as total from predicts));
end;
$$ LANGUAGE plpgsql;