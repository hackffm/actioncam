curl -X POST -H "application/json" -d '{"add": { "recording": "1_motion_20190219204453.avi"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "recording": "1_motion_20190219204447.avi"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "preview": "1_record_20200111195037", "1_record_20200111195037.avi"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "compressed": "20190818172955.zip"}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "compressed2recording": { "compressed": "20190818172955.zip", "recording": "1_motion_20190219204453.avi"}}}' http://localhost:8081/database
curl -X POST -H "application/json" -d '{"add": { "compressed2recording": { "compressed": "20190818172955.zip", "recording": "1_motion_20190219204447.avi"}}}' http://localhost:8081/database

curl -X  GET -H "application/json"  -d '{"query": {"recording_id": "1_motion_20190219204453.avi"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed_id": "20190818172955.zip"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed": "None"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed2recording": "20190818172955.zip"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed2recording": "1_motion_20190219204453.avi"}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"compressed2recording": "1_motion_20190219204447.avi"}}' http://localhost:8081/database

curl -X  GET -H "application/json"  -d '{"query": {"state": "None"}}' http://localhost:8081/database
curl -X  PUT -H "application/json"  -d '{"update": {"state": {"date_start": "20190922184919", "mode": "test", "previews_start": "1"}}}' http://localhost:8081/database

curl -X POST -H "application/json" -d '{"add": { "send": {"compressed": "20190818172955.zip", "seize": "5000", "receiver": "test@test.com", "date": "2019-09-24 10:26:07" }}}' http://localhost:8081/database
curl -X  GET -H "application/json"  -d '{"query": {"send": "None"}}' http://localhost:8081/database

curl -X  GET -H "application/json"  -d '{"query": {"report": "None"}}' http://localhost:8081/database