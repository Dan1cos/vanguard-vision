source .env
docker exec -it vanguard-vision-postgres psql -U $POSTGRES_USER -d $POSTGRES_DB
#in postgres terminal run:
\dt
\d item_type;
\d found_items;
SELECT * FROM item_type;
SELECT * FROM found_items;
exit
