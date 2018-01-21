import json
import urllib.parse
from urllib.request import urlopen
import random
from lxml import html
import time

#data = json.load(open("../data/training_data.json"))

# aggregating Nouns, Verbs, and Adjectives
# for arr in data:
#     pos_tag = arr[1]
#     text = arr[0]
#     if pos_tag == "NOUN" or pos_tag == "VERB" or pos_tag == "ADJ":
#         dct_pos[pos_tag].append(text);

def random_sonnet(dct_pos):
    form_data = {
        "type": 4,
        "spam_check": ""
    }

    #populate love/hate
    form_data["love_hate"] = random.choice(["love", "hate"])

    #populate noun
    form_data["noun"] = random.choice(dct_pos["NOUN"]);

    #populate aspects
    for i in range(1, 4):
        key = "aspect" + str(i)
        form_data[key] = random.choice(dct_pos["NOUN"]);

    #populate verb
    for i in range(1, 4):
        key = "verb" + str(i)
        form_data[key] = random.choice(dct_pos["VERB"])

    #populate adjective
    for i in range(1, 9):
        key = "aspect" + str(i)
        form_data[key] = random.choice(dct_pos["ADJ"])

    #populate month
    form_data["month"] = "August"
    form_data["to_notify"] = ""

    #populate writer
    form_data["writer"] = "deeps"

    encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
    #print(encoded_data)
    content = urlopen("https://www.poem-generator.org.uk/add_creation.php?action=send", encoded_data)

    full_content = ""

    for line in content.readlines():
        full_content += line.decode("utf-8")

    tree = html.fromstring(full_content)
    output = tree.xpath('//div[@class="poem"]/text()')

    parsed_output = [x.strip() for x in output]
    #print(parsed_output)

    num_values = 0
    string = ""

    for item in parsed_output:
        if num_values == 4:
            num_values = 0
            string = string[:-5]
            string += "\n"

        if item:
            string = string + item + " EOS "
            num_values += 1;

    string = string[:-5]
    return string

dct_pos = {"NOUN": [], "VERB": [], "ADJ": []}

with open("../data/training_data.json") as f:
    for line in f.readlines():
        if line != "\n":
            data = json.loads(line);
            for arr in data:
                pos_tag = arr[1]
                text = arr[0]
                if pos_tag == "NOUN" or pos_tag == "VERB" or pos_tag == "ADJ":
                    dct_pos[pos_tag].append(text);

with open("test.qtr", "a") as f:
    for i in range(2000):
        #print("getting random sonnet")
        print(i)
        sonnet = random_sonnet(dct_pos)
        #print(sonnet)
        f.write(sonnet);
        f.write("\n");
        f.write("\n");
        time.sleep(0.5)



