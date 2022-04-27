# Clock / Websocket

## Pitch

L'idée de base tourne autour d'un système d'aspersion automatique. Des capteurs remontent
des data à un système qui après va déclencher l'irrigation. L'utilisateur peut voir les infos sur une page web dédiés.

Pour l'exemple, on se contrentre sur la fonctionnalité suivante : 
Un horloge sur laquelle on peut voir l'etat du système (en cours de fonctionnement ou pas) et sur laquelle on 
peut voir l'historique de fonctionnement (les 10 dernières actions).

L'utilisateur peut controler le déclenchement via deux actions : 
 - un timer de X seconds (10 pour l'exemple)
 - um mode manuel avec durée indéfinie
Dans tout les cas il peut stopper l'actions en cours ou forcer le mode manuel

Les données transmises au client via push websocket sont : 
 - le timestamp courant (pas de notion de timezone - timestamp local)
 - le mode de l'action courante : timer, manuel, wait (pas d'aspersion)
 - le timestamp de début de l'action courante (timer et manuel)
 - le timestamp de fin de l'action courante (timer)

Les données sont transmises toute les secondes.

les changements de mode sont pilotés par HTTP via les endpoint 
 - `GET /manual`
 - `GET /timer`
 - `GET /stop`

L'historique est récupéré via HTTP sur le endpoint `GET /history`



## Improvement

Persistence de l'historique : pour l'exemple l'historique n'est pas persisté. Un minimum de persistence sur un support simple comme REDIS
permettrait d'être un peu plus propre.

Meilleur gestion des données transmise : l'objectif du websocket est de transmettre les infos d'état (mode, début et/ou fin) ET 
de transmettre l'info d'horloge (pour assurer que les données temporelle sont cohérentes - prendre l'exemple d'un système on premise non connecté sur internet pour lequel on ne maîtrise pas la synchronisation horaire). Dans l'exemple toutes les données sont tout le temps transmise.
Il serait judicieux d'avoir des transmissions différentes pour ne transmettre que l'info qui change au moment ou elle change.

Prévoir un support multi-système : pour l'exemple tout les devices se connecte sur le même channel et gère le même état.
Il faudrait rajouter un support multi channel (peut-etre socketIO qui intègre plus nativement ce type de mécanisme mais je ne suis pas convaincu). 

Améliorer le broadcast : pour l'exemple le système de broadcast est fait de manière assez naive, ce qui pose probablement des soucis de scaling.



## WS Server

Bootstrap the project :
```shell
make prepare-ws-server
```
Run it :
```shell
make run-ws-server
```

Test it :
```shell
websocat ws://localhost:8001
```

## React Clock

Bootstrap the project :
```shell
make prepare-react-clock
```

Run it :
```shell
make run-react-clock
```

test it :
```shell
open http://localhost:3000
```
