#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 fn"
    exit 1
fi
    
fn=$1
python simulation.py > $1

cn1=$(grep -o "Slacker" $fn | wc -l)
cn2=$(grep -o "Hunter" $fn | wc -l)
cn3=$(grep -o "RandomPlayer" $fn | wc -l)
cn4=$(grep -o "NormalThresholdPlayer" $fn | wc -l)
cn5=$(grep -o "ChaoticThresholdPlayer" $fn | wc -l)
cn6=$(grep -o "ReverseThresholdPlayer" $fn | wc -l)
cn7=$(grep -o "Helper" $fn | wc -l)

echo "python output to $fn"
echo "Slacker:		$cn1"
echo "Hunter:			$cn2"
echo "Helper:			$cn7"
echo "RandomPlayer:		$cn3"
echo "NormalThresholdPlayer:	$cn4"
echo "ChaoticThresholdPlayer:	$cn5"
echo "ReverseThresholdPlayer:	$cn6"

exit 0
