/*
select l_name,count(*) as pt_count,array_to_string(array_agg(p_id),',') as pt_list
from
(select l.name as l_name,p.id as p_id from
nw_line l, nw_point p
where ST_Distance(p.geom,l.geom)<0.000001
order by l.name,ST_Line_Locate_point(l.geom,ST_ClosestPoint(l.geom,p.geom))
) t
group by l_name
order by l_name;
*/