FROM huggingface/transformers-pytorch-gpu
COPY requirements.txt .
RUN python3.8 -m pip install -r requirements.txt
COPY output/aiwanger/* ./output/aiwanger/
COPY tweet.py \
  generate.py \
  .env ./
CMD python3 tweet.py | echo