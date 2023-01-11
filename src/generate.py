import argparse
import logging
import os
import random
from dataclasses import dataclass

import numpy as np
import torch
import re

from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    AutoTokenizer
)

def set_seed(args):
  np.random.seed(args.seed)
  torch.manual_seed(args.seed)
  if args.n_gpu > 0:
    torch.cuda.manual_seed_all(args.seed)

def sample_prompt(args):
  with open(args.model_name_or_path+"/startwords.txt") as f:
    l = f.readlines()
  return random.choice(l).strip().capitalize()

def filter(gen):
  return [g for g in gen if len(g) > 16]

def tweetify(generated_sequence):
  # Cut to 144
  x = generated_sequence[:min(len(generated_sequence), 144)]
  return x

@dataclass
class Args:
  """
  Settings container for the generation.
  """
  model_name_or_path = 'model_path'
  device = 'cpu'
  seed = 123
  fp16=False

  # Arguments for generation
  prompt=False
  prefix=""
  length=36
  temperature=1.0
  k=10
  p=.9
  repetition_penalty=2.0
  do_sample=True
  num_return_sequences=3
  length=144
  stop_token="<|endoftext|>"

def generate(prompt=False):
  """
  Generate tweets from a trained model

  Args:
      prompt (str|bool): Initial prompt word(s) for generating tweets. Defaults to False.

  Returns:
      list: list of <str> containing generated tweets
  """

  args = Args()
  args.prompt=prompt
  tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)
  model = GPT2LMHeadModel.from_pretrained(args.model_name_or_path)
  model.to(args.device)  
  if args.fp16:
    model.half()

  # Prompt
  prompt_text = args.prompt if args.prompt else sample_prompt(args)
  encoded_prompt = tokenizer.encode(args.prefix + prompt_text, add_special_tokens=False, return_tensors="pt")
  encoded_prompt = encoded_prompt.to(args.device)
  if encoded_prompt.size()[-1] == 0:
      input_ids = None
  else:
      input_ids = encoded_prompt

  output_sequences = model.generate(
    input_ids=input_ids,
    max_length=args.length + len(encoded_prompt[0]),
    temperature=args.temperature,
    top_k=args.k,
    top_p=args.p,
    repetition_penalty=args.repetition_penalty,
    do_sample=True,
    num_return_sequences=args.num_return_sequences,
  )

  generated_sequences = []
  print(f"Prompt: {args.prompt}")
  for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
    generated_sequence = generated_sequence.tolist()
    text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)
    # Remove all text after the stop token
    text = text[: text.find(args.stop_token) if args.stop_token else None]
    # Add the prompt at the beginning of the sequence. Remove the excess text that was used for pre-processing
    total_sequence = (
        prompt_text + text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True)) :]
    )
    generated_sequences.append(total_sequence)
    seq = filter(generated_sequences)
    seq = [tweetify(g) for g in seq]

  return seq

if __name__ == "__main__":
  print("Generating") 
  twts = generate("Das")
  print(twts)

