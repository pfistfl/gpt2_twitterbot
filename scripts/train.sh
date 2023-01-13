#!/bin/sh
python3 src/run_clm.py \
    --output_dir=model \
    --overwrite_output_dir \
    --overwrite_cache \
    --model_type=gpt2 \
    --model_name_or_path=dbmdz/german-gpt2 \
    --do_train --train_file=data/train.txt \
    --do_eval --validation_file=data/valid.txt \
    --eval_steps=20 \
    --logging_steps=20 \
    --per_device_train_batch_size=1 \
    --num_train_epochs=3 \
    --block_size=256
