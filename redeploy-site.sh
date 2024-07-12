#!/bin/bash
tmux kill-server
tmux new-session -d -s new-deployment
tmux send-keys -t new-deployment:0 'cd mlh-portfolio' C-m
tmux send-keys -t new-deployment:0 'git fetch && git reset origin/main --hard' C-m
tmux send-keys -t new-deployment:0 'source python3-virtualenv/bin/activate' C-m
tmux send-keys -t new-deployment:0 'pip install -r requirements.txt' C-m
tmux send-keys -t new-deployment:0 'flask run --host=0.0.0.0' C-m