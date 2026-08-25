SELECT m.measurement_date, ms.station_code, ms.station_name, ms.address, ms.latitude, ms.longitude, 
MAX(CASE WHEN mi.item_code=1 THEN m.average_value END) as SO2,
MAX(CASE WHEN mi.item_code=3 THEN m.average_value END) as NO2,
MAX(CASE WHEN mi.item_code=5 THEN m.average_value END) as CO,
MAX(CASE WHEN mi.item_code=6 THEN m.average_value END) as O3,
MAX(CASE WHEN mi.item_code=8 THEN m.average_value END) as PM10,
MAX(CASE WHEN mi.item_code=9 THEN m.average_value END) as "PM2.5"
FROM
"souel_station"."measurement" m 
JOIN "souel_station"."measurement_item" mi 
on m.item_code=mi.item_code
JOIN "souel_station"."measurement_station" ms
ON m.station_code=ms.station_code
GROUP BY m.measurement_date, ms.station_code, ms.station_name, ms.address, ms.latitude, ms.longitude