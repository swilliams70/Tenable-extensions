import requests

#global use variables  
access_key = 'foo'
secret_key = 'foo'
headers = {"Accept": "application/json", 'X-APIKeys': 'accessKey={}; secretKey={}'.format(access_key, secret_key)}
base_url = "foo"


#get group list
def get_groups():
    url = (base_url + "/agent-groups")
    method = "GET"
    response = requests.request(method, url, headers = headers)
    #print(response.json())

    groups = response.json().get('groups')

    group_list = []

    for group in groups:
        group_list.append(group.get('name'))


    print(group_list)

def get_agent(name):
    data = {'limit': 1, 'filter.0.filter': 'name', 'filter.0.quality': 'match', 'filter.0.value': name}
    url = (base_url + "/agents")
    method = "GET"
    response = requests.request(method, url, json = data, headers = headers)
    agents = response.json().get('agents')
    #print(agents)
    for agent in agents:
        uuid = agent.get('uuid')
        print(uuid)

    return uuid



#call it
#get_groups()
#get_agent()

name = 'foo'
uuid = get_agent(name)

#print(uuid)

