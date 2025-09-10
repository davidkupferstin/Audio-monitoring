import os
import  json
from services.classification.decryption import decrypt

from dotenv import load_dotenv

load_dotenv()

class PodcastClassification:
    def __init__(self):
        self.list_hostile = decrypt(os.getenv("LIST_HOSTILE")).lower().split(',')
        self.list_less_hostile = decrypt(os.getenv("LIST_LESS_HOSTILE")).lower().split(',')


    def number_of_words_in_podcast(self, text):
        count = 0

        for i in self.list_hostile:
            count_value = text.lower().count(i)
            if count_value > 0:
                count += count_value * 2

        for i in self.list_less_hostile:
            count_value = text.lower().count(i)
            if count_value > 0:
                count += count_value

        num_of_words = count
        return num_of_words

    def Calculating_hostility_percentages_podcast(self, num_of_words):
        # Each word adds 5% while a more hostile word that is counted twice adds 10%.
        danger_perce = num_of_words * 5
        return danger_perce


    def criminalize_podcasting(self, danger_perce):
        if danger_perce >= 80:
            criminal_podcast = True
        else:
            criminal_podcast = False
        return criminal_podcast

    def podcast_severity_rating_by_three_boundaries(self, danger_perce):
        if danger_perce <= 10:
            podcast_severity = "none"
        elif 10 <= danger_perce <= 45:
            podcast_severity = "medium"
        else:
            podcast_severity = "high"
        return podcast_severity


    def classification(self, podcast):
        text = podcast
        num_of_words = self.number_of_words_in_podcast(text)

        danger_perce = self.Calculating_hostility_percentages_podcast(num_of_words)

        criminal_podcast = self.criminalize_podcasting(danger_perce)

        podcast_severity = self.podcast_severity_rating_by_three_boundaries(danger_perce)

        classi_string = {"classification" : {
            "danger_perce" : f"{danger_perce} %",
            "criminal_podcast" : criminal_podcast,
            "podcast_severity" : podcast_severity
        }
        }

        classi_dict = json.dumps(classi_string, indent=4)
        return classi_dict





