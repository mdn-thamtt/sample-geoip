curl -X PUT "http://localhost:9200/_ingest/pipeline/geoip?pretty" -H 'Content-Type: application/json' -d'
{
  "description" : "Add geoip info",
  "processors" : [
    {
      "geoip" : {
        "field" : "ip"
      }
    }
  ]
}
'

----

curl -X PUT "http://localhost:9200/_ingest/pipeline/geoip?pretty" -H 'Content-Type: application/json' -d'
{
  "description" : "Add geoip info",
  "processors" : [
    {
      "geoip" : {
        "field" : "ip",
        "target_field" : "geo",
        "database_file" : "GeoLite2-Country.mmdb"
      }
    }
  ]
}
'

----

curl -X PUT "http://localhost:9200/_ingest/pipeline/geoip?pretty" -H 'Content-Type: application/json' -d'
{
  "description" : "Add geoip info",
  "processors" : [
    {
      "geoip" : {
        "field" : "ip",
        "target_field" : "geo",
        "database_file" : "GeoLite2-City.mmdb"
      }
    }
  ]
}
'

----

curl -X PUT "http://localhost:9200/user_ip/_doc/my_id?pipeline=geoip&pretty" -H 'Content-Type: application/json' -d'
{
  "ip": "89.160.20.128"
}
'

----

curl -X GET "http://localhost:9200/user_ip/_doc/my_id?pretty"

