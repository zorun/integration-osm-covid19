# Import des données de Dokomaps pour enrichir OSM et en particulier caresteouvert.fr
# https://github.com/osmontrouge/caresteouvert/issues/81
#
# Usage :
#
# conflate dokomaps_profile.py -i data-in/donnees.csv -l data-out/dokomaps-match.csv -o data-out/dokomaps.osm -c data-out/dokomaps.json

# Champ  "source" du changeset
source = 'dokomaps.com'

# Regexp moche Overpass API pour avoir tous les types de POI gérés par caresteouvert + restaurants
query = '[~"^(amenity|shop|craft|office)$"~"^(restaurant|pharmacy|post_office|fuel|supermarket|convenience|frozen_food|greengrocer|butcher|seafood|cheese|bakery|pastry|beverages|wine|alcohol|farm|deli|tobacco|e-cigarette|car_rental|bicycle|mobile_phone|doityourself|craft|optician|electronics|hardware|stationery|medical_supply|laundry|dry_cleaning|kiosk|pet|car_repair|car_parts|agrarian|newsagent|marketplace|bank|optician|electronics_repair|employment_agency|insurance|financial)$"]'

# Les valeurs de ces tags remplacent les valeurs des objets OSM.
#master_tags = ('ref',)

# Regarder au maximum 50 mètres autour d'un point du jeu de données.
max_distance = 50

# Par défaut, on regarde seulement 10 points proches, pas énorme pour des zones denses
nearest_points = 20

# pour permettre les points groupés
duplicate_distance = 0

# Pas d'ID
no_dataset_id = True


# Compare names to see if they partially match after normalization
def matches(osm_obj, dataset_obj):
    import unidecode
    def _normalize(s):
        return unidecode.unidecode(s).lower().translate(str.maketrans("", "", '\'":;,.!?=+%@^/[](){}$*~#&_- '))
    if 'name' not in osm_obj or 'note:name' not in dataset_obj:
        return False
    osm_name = _normalize(osm_obj['name'])
    dataset_name = _normalize(dataset_obj['note:name'])
    dataset_city = _normalize(dataset_obj['note:city'])

    # Cas particulier des bureaux de poste, qui ne contiennent visiblement pas "poste" dans leur nom.
    if "post" in dataset_name and osm_obj.get('amenity') == 'post_office':
        #print("POSTE", dataset_obj['note:name'], dataset_name)
        return True
    # Pas mal de faux positifs où le nom OSM est juste le nom de la ville,
    # notamment les bureaux de poste.
    if dataset_city == osm_name:
        return False
    # Cas le plus courant : le nom OSM contient le nom du jeu de données, ou l'inverse.
    if osm_name in dataset_name or dataset_name in osm_name:
        #print(dataset_obj['note:name'], dataset_name, osm_obj['name'], osm_name)
        return True
    # Même chose avec brand
    if 'brand' in osm_obj:
        brand = osm_obj['brand']
        if dataset_name in brand:
            #print(dataset_obj['note:name'], dataset_name, osm_obj['name'], osm_name)
            return True
    # Pas mal de POI ont une adresse dans le champ nom...  On trouve le
    # nom au début de la description.
    if 'note:comment' in dataset_obj:
        # On ne garde que les deux premiers mots de la description
        desc = _normalize(' '.join(dataset_obj['note:comment'].split()[:2]))
        # On évite les matches trop courts (type "de la")
        if len(desc) >= 5 and desc in osm_name or osm_name in desc:
            #print("DESC", desc, dataset_obj['note:comment'].split('\n')[0], "  |  ", osm_obj['name'], osm_name)
            return True
    # Génère trop de faux positifs...
    #import difflib
    #if difflib.get_close_matches(dataset_name, [osm_name]):
    #    return True
    return False

# A list of SourcePoint objects. Initialize with (id, lat, lon, {tags}).
def dataset(fileobj):
    import logging
    import csv
    #réouverture du fichier en mode texte
    fname = fileobj.name
    fileobj.close()
    fileobj = open(fname, 'r')
    csv_in = csv.reader(fileobj)
    data = []
    n = 0
    # Skip header
    next(csv_in)
    for row in csv_in:
        n += 1
        try:
            city = row[0]
            name = row[1]
            addr = row[2]
            lat = float(row[3])
            lon = float(row[4])
            comment = row[5]
            # Attention, on se sert aussi de ces tags dans la fonction `matches` !
            tags = {
                'note:name': name,
                'note:address': addr,
                'note:city': city,
            }
            # Le commentaire contient le statut d'ouverture, des horaires,
            # des infos de contact, et parfois bien plus...
            if comment:
                tags['note:comment'] = comment
            data.append(SourcePoint(n, lat, lon, tags))

        except Exception as e:
            logging.warning('PROFILE: Failed to get attributes : %s', str(e))  

    return data        
