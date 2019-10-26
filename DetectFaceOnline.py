import requests
import operator
from api import api_url, subscription_key


assert subscription_key


headers = {'Ocp-Apim-Subscription-Key': subscription_key}


params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'gender,emotion',
}


# image_url = 'https://a.uguu.se/LbWa0zKStxaC_2.jpg'
# image_url = 'https://a.uguu.se/PuzmfPLqmVZ3_3.jpg'
# image_url = 'https://a.uguu.se/NfMlKQQpJHtM_7.jpg'
# image_url = 'https://a.uguu.se/IVAklOKF3uAR_9.jpg'
# image_url = 'https://a.uguu.se/mgTU3Re3aBMt_11.jpg'


response = requests.post(api_url, params=params, headers=headers,
                         json={"url": image_url})


faceAttributes = []
gender = []
emotion_dic = []
emotions = []


for i in range(len(response.json())):
    faceAttributes.append(response.json()[i]['faceAttributes'])
    gender.append(faceAttributes[i]['gender'])
    emotion_dic.append(faceAttributes[i]['emotion'])


for i in range(len(emotion_dic)):
    emotions.append(max(emotion_dic[i].items(), key=operator.itemgetter(1))[0])


print(f'Total People :- {len(emotions)}')
print(f'Gender :- {gender}')
print(f'Emotions :- {emotions}')
