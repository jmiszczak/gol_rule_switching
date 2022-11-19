#!/bin/bash
expName=${0/.sh/}
echo "[INFO] Running experiment: " $expName
echo -n "[INFO] Start time: "
date +"%H:%M"
netlogo-headless.sh --model life-rule-switching.nlogo --setup-file experiments.xml --table $expName.csv --experiment $expName
echo -n "[INFO] End time:"
date +"%H:%M"
