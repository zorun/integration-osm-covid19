#!/bin/sh

for data in data-out/*.json
do
    out_matched="${data/.json}-matched.json"
    out_unmatched="${data/.json}-unmatched.json"
    jq '{type: "FeatureCollection", features: .features|map(select(.properties.action == "modify"))}' "$data" > "$out_matched"
    jq '{type: "FeatureCollection", features: .features|map(select(.properties.action == "create"))}' "$data" > "$out_unmatched"
done
