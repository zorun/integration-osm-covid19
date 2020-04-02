#!/bin/sh

cd data-out
for data in *.json
do
    out_matched="matched/${data/.json}-matched.json"
    out_unmatched="unmatched/${data/.json}-unmatched.json"
    # On enlève le préfixe "tags." à cause d'un bug d'affichage dans umap quand la clé est trop longue
    jq '{type: "FeatureCollection", features: .features|map(select(.properties.action == "create"))} | walk(if type == "object" and has("tags.note:city") then with_entries(.key |= sub("^tags\\."; "")) else . end)' "$data" > "$out_unmatched"
    # Ici on remplace "tags." par "t." et on enlève "tags_new." pour la même raison
    jq '{type: "FeatureCollection", features: .features|map(select(.properties.action == "modify"))} | walk(if type == "object" and has("tags_new.note:city") then with_entries(.key |= sub("^tags_new\\."; "")) | with_entries(.key |= sub("^tags\\."; "t.")) else . end)' "$data" > "$out_matched"
done
