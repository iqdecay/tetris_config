# TETRIS CONFIG : Configuration Sigfox
Développé par Victor Nepveu, victor.nepveu@imt-atlantique.net
https://victor-nepveu.dev/

## Pré-requis :

- Python (version >= 3.6) ([installation Python](https://www.python.org/downloads/))
- docker ([installation docker](https://docs.docker.com/install/))
- docker-compose ([installation docker-compose](https://docs.docker.com/compose/install/))

## Définition des termes :

- *callback_receiver* : le serveur qui interagit directement avec Sigfox, reçoit les requêtes en downlink et
renvoie les configurations demandées par les balises
- *frontend_server* : le serveur qui fait tourner le site web auquel on accède via le navigateur. Il sert à afficher
les différentes informations sur les balises, et à sauvegarder les nouvelles configurations
- *backend* : le serveur qui stocke les informations reçue par *callback_receiver* et qui les présente au frontend.
Il sert aussi à stocker les configurations qui sont entrées à travers l'interface web pour pouvoir les servir à
*callback_receiver* quand celui-ci reçoit une demande de configuration de Sigfox

## Technologies :

- *callback_receiver* : le serveur est écrit en Python3 et utilise le module [twisted](https://twistedmatrix.com/) pour servir 
les requêtes http, et le module [requests](https://requests.readthedocs.io/) pour communiquer avec le backend
- *backend* : le serveur backend est écrit en Golang, et utilise le module [mux](https://github.com/gorilla/mux/) pour
servir les requêtes faites à l'API. Le choix d'avoir un serveur backend en Golang ET un serveur python était justifié
par le projet précedent, dont le code de *callback_receiver* est largement inspiré. Twisted n'étant pas adapté
au rôle d'API REST, il était nécessaire de rajouter un serveur auquel le *frontend* s'adresse.
Go est un langage léger, rapide à mettre en place, notamment pour des microservices comme celui-ci, avec une gestion
automatique des dépendances.
- *frontend_server* : le serveur fait tourner une version de développement de React, qui permet de conserver des logs
dans la console en cas d'erreur. La mise en place de l'infrastructure "Single Page application" aurait nécessité un serveur
Nginx par exemple, inutilement compliqué pour l'échelle de cette application qui ne sert que d'interface graphique
et non de site web "réel".

## Configuration :
- Fichier tetris.venv :
    Fixer les variables à la valeur désirée :
    - HTTP_PORT : le port (un entier) sur lequel le serveur HTTP écoute les requêtes de Sigfox 
    et qui donc doit être un port libre de la machine. C'est le port qui sera rentré dans l'interface 
    Sigfox lors de la configuration du callback
    - GO_PORT : le port (un entier) sur lequel le backend communiquera avec le frontend 
    et callback_receiver. Il n'y a généralement pas besoin de le modifier (défaut à 4000)
    - REACT_PORT : le port sur lequel le site web de configuration sera accessible sur le navigateur

Une fois que les variables sont fixées, faire dans le terminal :
```bash
source tetris.env
```


##Mise en place :
- Vérifier que les variables d'environnement sont bien configurées :
```bash
echo $HTTP_PORT
echo $GO_PORT
echo $REACT_PORT
```
Cela doit afficher les valeurs configurées au paragraphe précédent

- Vérifier que le daemon *docker* est lancé :
``docker ps``

Il doit s'afficher quelque chose qui ressemble à ça :
```bash
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```
>Si cela ne fonctionne pas, sur Linux faire :
``systemctl start docker``
- Ensuite :
```bashj
cd /chemin/vers/dossier
docker-compose build;
```
Ensuite, deux possibilités :

- ``docker-compose up`` pour le faire tourner dans un terminal qu'on laisse ouvert

ou 

- ``docker-compose -d up`` pour le faire tourner dans un terminal qu'on peut fermer

Pour vérifier que tout fonctionne :
```docker ps```
doit cette fois retourner quelque chose du type :
```bash
CONTAINER ID        IMAGE                             COMMAND                  CREATED             STATUS              PORTS                    NAMES
12ce076ee340        tetris_config_callback_receiver   "python -u -m server…"   7 seconds ago       Up 6 seconds        0.0.0.0:80->80/tcp   callback_receiver
9774789c6992        tetris_config_backend             "./goBackend"            7 seconds ago       Up 6 seconds        0.0.0.0:4000->4000/tcp   backend_server
679f558cb07b        tetris_config_frontend            "docker-entrypoint.s…"   37 minutes ago      Up 6 seconds        0.0.0.0:3000->3000/tcp   frontend_server
```

- Le serveur HTTP reçoit les requêtes sur le port précisé à l'étape de configuration

## Usage :

- L'interface web est accessible sur un navigateur à l'adresse [http://localhost:{REACT_PORT}] où {REACT_PORT} est 
la valeur configurée plus haut

- La page d'accueil liste les balises détectées. La liste est vide tant que une balise n'a pas 
envoyé de requête en uplink (via une demande de configuration ou un acknowledgement).

- Pour configurer une balise ou la renommer, il faut cliquer sur l'icône de l'engrenage correspondante. La configuration
est sauvegardée immédiatement dans le système, et sera servie à la balise à sa prochaine demande de configuration