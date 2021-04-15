import glob
import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt

# read in data
hep = []
for hermit_transcript in glob.glob("data/hep/*.pkl"):
    hermit = os.path.split(hermit_transcript)[-1].split('.')[0]
    with open(hermit_transcript, 'rb') as f:
        transcripts = pickle.load(f)
        hep.append({
            "name": hermit,
            "transcripts": transcripts
        })
resistance = []
for hermit_transcript in glob.glob("data/resistance/*.pkl"):
    hermit = os.path.split(hermit_transcript)[-1].split('.')[0]
    with open(hermit_transcript, 'rb') as f:
        transcripts = pickle.load(f)
        resistance.append({
            "name": hermit,
            "transcripts": transcripts
        })


# count mentions of war
war = [('hep', hep), ('resistance', resistance)]
rows = []
for side_str, side in war:
    for hermit in side:
        for i, transcript in enumerate(hermit['transcripts']):
            def get_count(text):
                return sum(map(text.lower().count, ("resistance", "war", "turf", "grass", "hep", "environment", "environmental", "mycelium")))
            rows.append({
                'date': transcript['date'],
                'hermit': hermit['name'],
                'allegiance': side_str,
                'count': get_count(transcript['text'])
            })

df = pd.DataFrame(rows)
df.to_csv('data/HCTurfWar.csv')

