FROM huggingface/transformers-pytorch-gpu
COPY requirements.txt .
RUN python3.8 -m pip install -r requirements.txt
COPY model/* ./model/
COPY src/tweet.py \
  src/generate.py \
  .env ./
CMD python3 tweet.py | echo