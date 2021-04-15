from pyyoutube import Api
from youtube_transcript_api import YouTubeTranscriptApi
import time
import re
import datetime
import pickle

##### CONSTANTS

api = Api(api_key='secret-key-goes-here')

# Groups from
# https://hermitcraft.fandom.com/wiki/Season_7_Turf_War#Groups

hep = {
    'GoodTimesWithScar': 'UCodkNmk9oWRTIYZdr_HuSlg',
    'Cubfan135': 'UC9lJXqw4QZw-HWaZH6sN-xw',
    'Xisumavoid': 'UCU9pX8hKcrx06XfOB-VQLdw',
    'BdoubleO100': 'UClu2e7S8atp6tG2galK9hgg',
    'TangoTek': 'UC4YUKOBld2PoOLzk0YZ80lw',
    'Keralis': 'UCcJgOennb0II4a_qi9OMkRA',
    'FalseSymmetry': 'UCuQYHhF6on6EXXO-_i_ClHQ'
}

resistance = {
    'Grian': 'UCR9Gcq0CMm6YgTzsDxAxjOQ',
    'ImpulseSV': 'UCuMJPFqazQI4SofSFEd-5zA',
    'Rendog': 'UCDpdtiUfcdUCzokpRWORRqA',
    'xBCrafted': 'UC_MkjhQr_D_lGlO3uu-GxyA',
    'Stressmonster101': 'UC24lkOxZYna9nlXYBcJ9B8Q',
    'docm77': 'UC4O9HKe9Jt5yAhKuNv3LXpQ',
    'EthosLab': 'UCFKDEp9si4RmHFWJW1vYsMA'
}

resistance_founded = '2020-08-13' # Hermitcraft 7: Episode 37 - RULES & BARGE BOXES
resistance_founded = time.strptime(resistance_founded, "%Y-%m-%d")

#####

for hermit, channel_id in hep.items():
    print("Processing ", hermit, '\n--------------------')
    playlists = [p.to_dict() for p in api.get_playlists(channel_id=channel_id, count=None).items]
    def find_season(playlist):
        name = playlist['snippet']['title']
        variations = [
            'season 7',
            'hermitcraft 7',
            'hermitcraft vii',
            's7'
        ]
        for variation in variations:
            if variation in name.lower():
                return True
        return False
        
    # get season playlist
    print('Getting season 7 playlist')
    season_playlist = list(filter(find_season, playlists))[0]
    print(season_playlist['snippet']['title'])

    # get episode ids
    print('Getting episode IDs after resistance')
    episodes = api.get_playlist_items(playlist_id=season_playlist['id'], parts=['snippet'], count=None).items
    def limit_by_date(episode):
        episode_date = episode.snippet.publishedAt[:10]
        episode_date_f = time.strptime(episode_date, "%Y-%m-%d")
        return episode_date_f >= resistance_founded

    episodes = list(filter(limit_by_date, episodes))

    # get captions
    print('Getting transcripts')
    transcripts = []
    for episode in episodes:
        id = episode.snippet.resourceId.videoId
        title = episode.snippet.title
        
        date = re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',episode.snippet.publishedAt)[0]
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        
        print("Retrieving transcript for: ", title, f" ({date})")
        try:
            transcripts.append({
                "title": title,
                "id": id,
                "date": date,
                "text": ' '.join([x["text"] for x in YouTubeTranscriptApi.get_transcript(id)])
            }
            )
        except:
            print('\tCould not find transcript')

    with open(f'data/hep/{hermit}.pkl', 'wb') as f:
        pickle.dump(transcripts, f)

    print(f"--- Finished {hermit} ---")
    print("-------------------------")
