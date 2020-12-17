import requests
from pprint import pprint
import time

token = ''

class VkUser:
  url = 'https://api.vk.com/method/'
  def __init__(self, token, version):
    self.token = token
    self.version = version
    self.params = {'access_token': self.token, 'v': self.version}

    self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

  def __str__(self):
    return f'http://vk.com/id{self.owner_id}'


  def get_mutual_friends(self, source_uid=None, target_uid=0):
    if source_uid is None:
        source_uid = self.source_uid
    self.source_uid = source_uid
    self.target_uid = target_uid
    mutual_friends_url = self.url + 'friends.getMutual'
    self.mutual_friends_params = {'source_uid': self.source_uid, 'target_uid': self.target_uid}
    mutual_friends = requests.get(mutual_friends_url, params={**self.params, **self.mutual_friends_params}).json()['response']

    friends_url = self.url + 'users.get'
    friends_list = []

    for id in mutual_friends:
      resp = requests.get(friends_url, params={**self.params,'user_ids': id, 'fields': 'nickname'}).json()#['response']['items']
      time.sleep(0.4)
      friends_list.append(resp)

    return friends_list


  def __and__(self, other):
    if not isinstance(other, VkUser):
        raise NotImplementedError('Can not be compared with VkUser')

    return self.get_mutual_friends(source_uid=self.owner_id, target_uid=other.owner_id)

user1 = VkUser(token, '5.126')
user1.owner_id = 6492
user2 = VkUser(token, '5.126')
user2.owner_id = 2745

pprint(user1 & user2)

print(user2)