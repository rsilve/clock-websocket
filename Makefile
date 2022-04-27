prepare: prepare-ws-server prepare-react-client

prepare-ws-server: ws-server
	cd $<; python3 -mvenv .env; .env/bin/pip install -r requirements.txt;

prepare-react-client: react-clock
	cd $<; npm install;

run-ws-server: ws-server
	cd $<; .env/bin/python3 server.py

run-react-clock: react-clock
	cd $<; npm run dev