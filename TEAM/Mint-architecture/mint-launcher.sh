#!/bin/bash

function main () {
	if [ $# -lt 4 ]; then	# if less than 4 arguments
		echo "Usage: $0 path/to/architecture/program N1 N2 problem-solver1 [ problem-solver2 […]]"
		exit 0
	fi
	architecture="${1}"; shift
	N1="${1}"; shift
	N2="${1}"; shift

	# create 2 temporary files
	exact_change=$(mktemp)
	exchange=$(mktemp)

	# while we haven't iterated over every argument
	while [ $# != 0 ]; do
		problem_solver=${1}; shift
		./timed-pipe "${problem_solver}" "${architecture}" "${N1}" 1 >> $exact_change
		./timed-pipe "${problem_solver}" "${architecture}" "${N2}" 2 >> $exchange
	done
	echo -e     "---------- EXACT CHANGE PROBLEM ----------\n"
	cat $exact_change | ./score-printer
	echo -e "\n\n------------ EXCHANGE PROBLEM ------------\n"
	cat $exchange | ./score-printer

	# cleanup
	rm $exact_change $exchange
}

main $*
