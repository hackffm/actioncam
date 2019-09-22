curl -X POST -H "application/json" -d '{"add": { "recording": "1_motion_20190219204453.avi"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "recording": "1_motion_20190219204447.avi"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "compressed": "20190818172955.zip"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "compressed2recording": ["20190818172955.zip", "1_motion_20190219204453.avi"]}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "compressed2recording": ["20190818172955.zip", "1_motion_20190219204447.avi"]}}' http://localhost:8081/database

curl -X  GET -H "application/json"  -d '{"query": {"recording_id": "1_motion_20190219204453.avi"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed_id": "20190818172955.zip"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed": "None"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed2recording": "20190818172955.zip"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed2recording": "1_motion_20190219204453.avi"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed2recording": "1_motion_20190219204447.avi"}}' http://localhost:8081/database

curl -X  GET -H "application/json"  -d '{"query": {"state": "None"}}' http://localhost:8081/database
curl -X  PUT -H "application/json"  -d '{"update": {"state": {"date_start": "20190922184919", "mode": "test", "previews_start": "1"}}}' http://localhost:8081/database
