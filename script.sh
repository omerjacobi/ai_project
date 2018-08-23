#!/bin/bash
# Setting a return status for a function
print_something () {

echo start a run of $1 trains on $3 agent
python2 gameInit.py --agent1=AlphaBetaAgent --agent2=NNAgent --train_agent=$3 --train_agent_heu=$2 --display=SummaryDisplay --num_of_training=$1 --num_of_games=2 --depth=2 & disown
p=$!
}
array=( 1000 10000 50000 200000 )
for i in "${array[@]}"
do
print_something $i Aggressive_Full AlphaBetaAgent
print_something $i Full AlphaBetaAgent
print_something $i Full RandomAgent
done

