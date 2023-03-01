import openai
import pandas as pd
import json

def openFile(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = '*********'


def gpt3_completion(prompt, engine='text-davinci-002', temp=1.0, tokens=1000):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    while True:
        try:
            response = openai.Completion.create(engine=engine, prompt=prompt, temperature=temp, max_tokens=tokens)
            text = response['choices'][0]['text'].strip()
            return text
        except Exception as e:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % e
            print('Error connecting to OpenAI:', e)


def createDataset(param1, param2, param3, input_filename, l1, l2, l3, prompt_response_list):
    c = 0
    prompt = openFile(input_filename)
    d = {}

    for x in l1:
        for y in l2:
            for z in l3:

                if c >= 50:
                    break

                prompt_s = prompt

                prompt_s = prompt_s.replace('<<'+param1+'>>', x)
                prompt_s = prompt_s.replace('<<'+param2+'>>', y)
                prompt_s = prompt_s.replace('<<'+param3+'>>', z)

                generated_email = gpt3_completion(prompt_s)

                d["prompt"] = prompt_s.rstrip() + '->'
                d['completion'] = generated_email

                prompt_response_list.append(d)
                c += 1


if __name__ == '__main__':
    
    meals = ['lentil based meal', 'gluten free meal', 'vegan meal', 'salads and soups', 'keto meal', 'low fat meal', 'high protein meal']
    reasons = ['weight loss', 'time constraints', 'healthy lifestyle',  'dietary constraints/allergies', 'try new exciting options'] 
    user_profiles = ['professional athlete', 'pregnant woman', 'post-surgery recovery patient', 'student on low budget', 'immuno compromised individual', 'lactose intolerant individual']
    subscriptions = ['monthly vegan plan', 'monthly keto plan', 'weekly high protein diet',  'weekly nutritious breakfast bowl', 'quarterly salad and soup combo', \
    'half-yearly gluten free lunch box', 'monthly high carbs breakfast']
    types = ['vegetarian', 'non-vegetarian']

    prompt_response_list = []

    createDataset('MEAL', 'USER_PROFILE', 'REASON', 'prompt_1.txt', meals, user_profiles, reasons, prompt_response_list)
    createDataset('MEAL', 'USER_PROFILE', 'SUBSCRIPTION', 'prompt_3.txt', meals, user_profiles, subscriptions, prompt_response_list)

    with open('dataset.json', 'w') as f:
        json.dump(prompt_response_list, f)

    
