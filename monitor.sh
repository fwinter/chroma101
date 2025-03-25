#!/bin/bash

delta_h=""
acc_prob=""

# Read input line-by-line
while IFS= read -r line; do
    # Check for Delta H
    if [[ "$line" =~ ^Delta\ H\ =\ ([0-9.eE+-]+) ]]; then
        delta_h="${BASH_REMATCH[1]}"
    fi

    # Check for AccProb
    if [[ "$line" =~ ^AccProb\ =\ ([0-9.eE+-]+) ]]; then
        acc_prob="${BASH_REMATCH[1]}"
    fi

    # When both values are captured, print and reset
    if [[ -n "$delta_h" && -n "$acc_prob" ]]; then
        echo "Delta H: $delta_h | AccProb: $acc_prob"
        delta_h=""
        acc_prob=""
    fi
done
