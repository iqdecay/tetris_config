# tetris-config : Configuration Sigfox et supervision
Code par Victor Nepveu, victor.nepveu@imt-atlantique.net
https://github.com/vnepveu/

## Pré-requis :

- Python (version >= 3.6) ([installation Python](https://www.python.org/downloads/))
- docker ([installation docker](https://docs.docker.com/install/))
- docker-compose ([installation docker-compose](https://docs.docker.com/compose/install/))

## Configuration :
Fichier tetris.venv :
Fixer les variables à la valeur désirée :
- HTTP_PORT : le port (un entier) sur lequel le serveur HTTP écoute les requêtes

Une fois que les variables sont fixées, faire dans le terminal :
```bash
source tetris.env
```

##Usage :
- Vérifier que les variables d'environnement sont bien configurées :
```bash
echo $HTTP_PORT
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

```docker ps```
doit cette fois retourner quelque chose du type :
```bash
CONTAINER ID        IMAGE                             COMMAND                  CREATED             STATUS              PORTS                    NAMES
38a96a2c6d46        tetris_config_callback_receiver   "python -u -m server…"   26 seconds ago      Up 2 seconds        0.0.0.0:8080->8080/tcp   callback_receiver

```


