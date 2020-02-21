from fbchat import Client, log
from fbchat.models import *
from time import time
import csv
import re
import os


co = {}
co["c_user"] =os.environ["c_user"]
co["datr"] =os.environ["datr"]
co["fr"] =os.environ["fr"]
co["sb"] =os.environ["sb"]
co["spin"] =os.environ["spin"]
co["xs"] =os.environ["xs"]
co["noscript"] = "1"

def csv_dict_list(variables_file):
    with open(variables_file, "r", encoding="utf-8") as out:
        reader = csv.DictReader(out)
        dict_list = []
        for line in reader:
            dict_list.append({"pattern": line["pattern"], "reponse": line["reponse"]})
        return dict_list
answers = csv_dict_list("reponses.csv")

class FbChat(Client):
    def onMessage(self, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))
		#check if the message is a text
        if message_object.text:
            text = message_object.text
            if thread_type != ThreadType.GROUP:
                if author_id != self.uid:
				#searching for answer to reply
                    for answer in answers:
                        if re.search(answer["pattern"],text,flags=re.IGNORECASE):
                            self.send(Message(text=answer["reponse"]), thread_id=thread_id, thread_type=thread_type)
                            break
        else:
		#if it's not a text then reply back the same message
            if author_id != self.uid:
                self.send(message_object, thread_id=thread_id, thread_type=thread_type)

#cookies (optional)
client = FBChat("email", "password", session_cookies=co)
client.listen()

