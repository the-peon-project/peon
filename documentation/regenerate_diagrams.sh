#!/bin/bash

# TODO: Check if `graphviz` installed else run yum install -y graphviz
# TODO: Check if `diagrams` installed else run pip install diagrams

diagram_path="./diagram_definitions/"

printf "Regenerating PEON Diagrams...\n"
total=$(find $diagram_path -type f -name "*.py" | grep -c ".py$")
i=0
for file in $diagram_path*.py; do
    ((i++))
    printf " - [$i/$total] $(basename $file .py)\n"
    python3 "$file"; 
done