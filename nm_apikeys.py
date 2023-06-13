import requests
import sys,getopt

#global use variables
apikey = open('apikey_nm.txt').read().splitlines()
access_key=apikey[0]
secret_key=apikey[1]
nm_host='[host]'
base_url = 'https://[]:8834'.format(nm_host)
headers = {'Accept': 'application/json', 'X-APIKeys': 'accessKey={}; secretKey={}'.format(access_key, secret_key)}

#get group list
def get_groups():
    url = (base_url + '/agent-groups')
    method = 'GET'
    response = requests.request(method, url, headers = headers)

    #print(response.request.method)
    #print(response.request.url)
    #print(response.request.body)
    #print(response.request.headers)

    groups = response.json().get('groups')

    group_list = []

    for group in groups:
        group_list.append(group.get('name'))

    return group_list
    
def get_agent_groups(name):
    data = {'limit': 1, 'filter.0.filter': 'name', 'filter.0.quality': 'match', 'filter.0.value': name}
    url = (base_url + "/agents")
    method = "GET"
    
    response = requests.request(method, url, json = data, headers = headers)
    agents = response.json().get('agents')

    for agent in agents:
        print("{},{}".format(agent.get('name'), agent.get('groups')))
    
def list_group_hosts(name):
    data = {'limit': 1, 'filter.0.filter': 'groups', 'filter.0.quality': 'match', 'filter.0.value': name}
    url = (base_url + "/agents")
    method = "GET"
    
    response = requests.request(method, url, json = data, headers = headers)
    agents = response.json().get('agents')
    
    
    #hosts = []
       
    #for agent in agents:
    #    hosts.append(agent.get('name'))
        
    #print(hosts)
    
    with open(r'out.txt', 'w') as fp:
        for agent in agents:
            # write each item on a new line
            item = agent.get('name')
            fp.write("%s\n" % item)
    print('Done')
    
    return

#do a name match search
def get_agent(name):
    data = {'limit': 1, 'filter.0.filter': 'name', 'filter.0.quality': 'match', 'filter.0.value': name}
    url = (base_url + "/agents")
    method = "GET"
    
    response = requests.request(method, url, json = data, headers = headers)
    agents = response.json().get('agents')
       
    uuid = []
    
    for agent in agents:
        uuid.append(agent.get('uuid'))
        
    #print(uuid)
    
    return uuid

#get a list of hosts and make a UUID list
def get_agent_list():
    agent_clusters = []
    agents = []
    with open('hosts.txt','r') as fileobj:
    
        #strip newlines when reading
        host_list = fileobj.read().splitlines()

        for name in host_list:
            agent_clusters.append(get_agent(name))
        for cluster in agent_clusters:
            for agent in cluster:
                agents.append(agent)

    return agents

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
       opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
       print ('test.py -i <inputfile> -o <outputfile>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print ('test.py -i <inputfile> -o <outputfile>')
          sys.exit()
       elif opt in ("-i", "--ifile"):
          inputfile = arg
       elif opt in ("-o", "--ofile"):
          outputfile = arg
    print ('Input file is "', inputfile)
    print ('Output file is "', outputfile)

    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print('Argument List:', str(sys.argv))

    #list groups
    #groups = get_groups()
    #for group in groups:
    #    print(group)
    
    #list of agent group membership
    #name = 'ltcp-swilliam21'
    #get_agent_groups(name)

    #list of agent UUIDs
    #agents = get_agent_list()
    #for agent in agents:
    #    print(agent)

    #list hosts in group
    #list_group_hosts('Servers - PRD')

if __name__ == '__main__':
    main(sys.argv[1:])

