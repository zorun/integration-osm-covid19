# Intégration données dokomaps

Cf. <https://github.com/osmontrouge/caresteouvert/issues/81>

## Outils

On utilise `osm_conflate` en python : <https://wiki.openstreetmap.org/wiki/OSM_Conflator>

Voir la [présentation de Jérôme Villafruela](https://github.com/JVillafruela/atelier-osm-conflator)
qui contient des instructions d'usage et plusieurs examples.

## Processus de conflation

Les données n'ont ni référence, ni d'indication sur leur type (restaurant, bureau de poste...)

On prend donc le parti de matcher le jeu de données avec les données OSM **uniquement à partir
des noms** (et de la position géographique bien sûr).

`osm_conflate` télécharge les données OSM sur l'ensemble de la bounding box du jeu de données.
Dans notre cas ça représente beaucoup trop de données, et c'est bête parce que l'emprise géographique
des données est au final assez faible (c'est très localisé par cluster).
On commence donc par séparer le jeu de données par « ville », et on lance `osm_conflate` sur chaque
ville indépendamment.

## En pratique

Un script fait la séparation par ville et lance la conflation sur chaque ville :

    ./conflate.sh

On obtient un geojson, un osm, et un CSV avec le résumé des matches, le tout dans `data-out`.

Attention, ça fait beaucoup d'appels à l'API Overpass et on peut vite se retrouver coincé !

## Exploitation des fichiers

Les données du jeu de données sont mises dans des tags `note:XXX`.

On peut charger les fichiers `.osm` dans JOSM, mais attention à faire le ménage dans les tags...

Pour splitter les geojson pour avoir d'un côté les points rapprochés et de l'autre les points
non rapprochés :

    ./split_conflated.sh

Ça crée des fichiers GeoJSON `-matched.geojson` et `-unmatched.geojson`.
On peut ensuite les charger dans umap ou JOSM.
