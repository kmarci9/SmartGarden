CREATE or REPLACE VIEW espview as
select temperature,soil from
espdata
order by created desc
limit 100