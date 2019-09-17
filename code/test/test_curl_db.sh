curl -X POST -H "application/json" -d '{"add": { "recording": "1_record_20190919100000.jpeg"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"query": { "recording": "1_record_20190919100000.jpeg"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "compressed": "20190818172955.zip"}}' http://localhost:8081/database