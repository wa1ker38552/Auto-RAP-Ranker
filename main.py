from alive import keepAlive
import requests
import time
import os

def get_rap(id):
  rap = 0
  request = requests.get(f'https://inventory.roblox.com/v1/users/{id}/assets/collectibles?sortOrder=Asc&limit=100').json()
  try:
    next_page = request['nextPageCursor']
    for item in request['data']:
      try:
        rap += item['recentAveragePrice']
      except TypeError: pass

    while next_page is not None:
      request = requests.get(f'https://inventory.roblox.com/v1/users/{id}/assets/collectibles?sortOrder=Asc&limit=100&cursor={next_page}').json()
      next_page = request['nextPageCursor']
      for item in request['data']:
        try:
          rap += item['recentAveragePrice']
        except TypeError: pass
    return rap
  except KeyError: pass

def get_members(id):
  users = []
  request = requests.get(f'https://groups.roblox.com/v1/groups/{id}/users?sortOrder=Asc&limit=100').json()
  next_page = request['nextPageCursor']
  for user in request['data']:
    users.append({
      'id': user['user']['userId'],
      'role': user['role']['name']
    })
  while next_page is not None:
    request = requests.get(f'https://groups.roblox.com/v1/groups/{id}/users?sortOrder=Asc&limit=100&cursor={next_page}').json()
    next_page = request['nextPageCursor']
    for user in request['data']:
      users.append({
        'id': user['user']['userId'],
        'role': user['role']['roleId']
      })
  return users

def refresh_xcsrf(token):
  response = requests.post('https://auth.roblox.com/v1/login', cookies={'.ROBLOSECURITY': token})
  if "X-CSRF-TOKEN" in response.headers:
    return response.headers["X-CSRF-TOKEN"]

def rank(user_id, group_id, rank_id):
  with requests.Session() as session:
    session.cookies['.ROBLOSECURITY'] = os.environ['TOKEN']
    headers = {'x-csrf-token': refresh_xcsrf(os.environ['TOKEN'])}
    data = {'roleId': rank_id}
    session.patch(f'https://groups.roblox.com/v1/groups/{group_id}/users/{user_id}', headers=headers, data=data)


group = groupid

keepAlive()
while True:
  members = get_members(group)
  for member in members:
    if member['role'] == ownerid: pass
    else:
      member_rap = get_rap(member['id'])
      if member_rap == 0 or member == None: pass
      elif member_rap in range(1000, 9999):
        rank(member['id'], group, rankid)
      elif member_rap in range(10000, 249999):
        rank(member['id'], group, rankid)
      elif member_rap in range(250000, 1000000):
        rank(member['id'], group, rankid)
      else:
        rank(member['id'], group, rankid)
  time.sleep(10)
  print('Refreshed group!', len(members))
