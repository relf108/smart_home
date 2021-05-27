echo 'run from smart_home_iot directory'
export FLASK_APP=cloud_server/app.py
flask run
python3 cloud_server/front_end_client.py
echo 'Now go to hud directory and run yarn start'
