DATE="20200331"

# On splitte
./split_dokomaps_data.py data-in/dokomaps_covid19_${DATE}_licence-odbl.csv data-in/cities-${DATE}.txt

# On conflate chaque zone
while read city
do
    data="data-in/dokomaps_covid19_${DATE}_licence-odbl-${city}.csv"
    matchfile="data-out/dokomaps-${DATE}-${city}.csv"
    changefile="data-out/dokomaps-${DATE}-${city}.json"
    osmfile="data-out/dokomaps-${DATE}-${city}.osm"
    printf "\nNow conflating $city\n"
    conflate dokomaps_profile.py -i "$data" -l "$matchfile" -o "$osmfile" -c "$changefile"
    # Overpass API a du rate-limiting
    sleep 5
done < data-in/cities-${DATE}.txt
