curl -X POST -H "application/json" -d '{"add": { "recording": "2_motion_20190219204453.avi"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "recording": "2_motion_20190219204447.avi"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "compressed": "20190818172955.zip"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "compressed2recording": ["20190818172955.zip", "2_motion_20190219204453.avi"]}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "compressed2recording": ["20190818172955.zip", "2_motion_20190219204447.avi"]}}' http://localhost:8081/database

curl -X  GET -H "application/json"  -d '{"query": {"recording_id": "2_motion_20190219204453.avi"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed_id": "20190818172955.zip"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed": "None"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed2recording": "20190818172955.zip"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed2recording": "2_motion_20190219204453.avi"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed2recording": "2_motion_20190219204447.avi"}}' http://localhost:8081/database
