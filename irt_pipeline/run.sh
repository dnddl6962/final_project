#!/bin/bash

python main.py

py-irt train 2pl test1.jsonlines test-2pl/ --lr 0.1 --epochs 2000

python main2.py
