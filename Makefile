prepare-ws-server: ws-server
	cd $<; python3 -mvenv .env; .env/bin/pip install -r requirements.txt;

run-ws-server: ws-server
	cd $<; .env/bin/python3 server.py