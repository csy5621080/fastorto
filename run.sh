#!/usr/bin/zsh

cd /home/chengsy/Project/fastApiLearn/

exec /home/chengsy/virtualenvs/fast-api/bin/uvicorn main:app --host 0.0.0.0 --port 8050