#! /bin/bash

pip3 install -r requirements.txt
result=$(python3 <<EOF
from app import app
print('all $code in one very long line')
EOF
)

