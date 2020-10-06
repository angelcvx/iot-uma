from z3 import *
from random import randint
import time
import random
import string
import statistics

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

communicationCost = Real('communicationCost')
communicationCostDown = Real('communicationCostDown')
computationCost = Real('computationCost')
communicationTime = Real('communicationTime')
computationTime = Real('computationTime')

nUsers = 1

print('**Welcome to the Benchmark version of the Optimal Task Assignment Framework (OTAF)** \n')
nTask = int(input('Enter the number of tasks: '))
nNodes = int(input('Enter the number of devices: '))

nFeaturesLocated = round(nTask*random.uniform(0.10,0.15))
nFeatures = nTask - nFeaturesLocated
nConstraints = round(random.uniform(0.1,0.3)*nFeatures)

assignment = [ [ Bool("ASING_%s_%s" % (r,c)) for c in range(nNodes+nUsers-1) ] 
      for r in range(nTask*nUsers) ]


#data to be transmitted between tasks
relation = [ [ 0 for c in range(nTask) ] 
      for r in range(nTask) ]

for n in range(nFeatures - 1):
	relation[nFeaturesLocated + n][nFeaturesLocated+ n+1] = random.uniform(30/8,30000/8)

tasks = [ [ 0 for c in range(9) ] 
      for r in range(nTask) ]

nodes = [ [ 0 for c in range(14) ] 
      for r in range(nNodes) ]


def randomString(stringLength=2):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))	

for x in range(0, nFeaturesLocated):
	location = randomString()
	tasks[x][0] = 10 #CameraCalibration
	tasks[x][1] = 10
	tasks[x][2] = x
	tasks[x][3] = 0
	tasks[x][4] = {''}
	tasks[x][5] = {''}
	tasks[x][6] = {}
	tasks[x][7] = location
	tasks[x][8] = 'mote'

	nodes[x][0] = 10
	nodes[x][1] = 10
	nodes[x][2] = 0.1
	nodes[x][3] = 0.00023
	nodes[x][4] = 6000
	nodes[x][6] = 0.1
	nodes[x][7] = 250000000
	nodes[x][8] = {''}
	nodes[x][9] = {''}
	nodes[x][10] = 'mote'
	nodes[x][11] = location
	nodes[x][12] = 'public'
	nodes[x][13] = {'wlan'}


for x in range(nFeaturesLocated, nTask):
	tasks[x][0] = random.uniform(120,2400)
	tasks[x][1] = random.uniform(10,100)
	tasks[x][2] = x
	tasks[x][3] = 0
	tasks[x][4] = {''}
	tasks[x][5] = {''}
	tasks[x][6] = {}
	tasks[x][7] = 'none'
	tasks[x][8] = 'computing'


for x in range(nFeaturesLocated, nNodes):
	nodes[x][0] = random.uniform(1000000000,2400000000)
	nodes[x][1] = random.uniform(150000000,200000000)
	nodes[x][2] = random.uniform(0.3,0.4)
	nodes[x][3] = random.uniform(0.00000003,0.0000005)
	nodes[x][4] = random.uniform(2000,6000)
	nodes[x][6] = random.uniform(0.2,0.4)
	nodes[x][7] = random.uniform(150000000,200000000)
	nodes[x][8] = {''}
	nodes[x][9] = {''}
	nodes[x][10] = 'computing'
	nodes[x][11] = 'anyplace'
	nodes[x][12] = 'public'
	nodes[x][13] = {'wlan'}

#Edges of the task-call graph
constraints = [ [ 0 for c in range(nTask) ] 
      for r in range(nConstraints) ]

#[0] max time to be executed
#[1] number of tasks involved in the restriction
#[2...n] index of the involved tasks
#create random time restrictions 
for n in range(nConstraints):
	aux = round(random.uniform(0.2,0.5)*nFeatures)
	constraints[n][0] = random.uniform(0.8,5)
	constraints[n][1] = aux
	featureIni = random.uniform(0,nFeatures-aux)
	for x in range(aux):
		constraints[n][aux+2] = x + featureIni + nFeaturesLocated
		

def getDistance(lat1,lon1,lat2,lon2,connectivity, range):
		R = 6373.0
		dlon = lon2 - lon1
		dlat = lat2 - lat1

		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))

		distance = R * c
		available = distance < range

		return available


def numberUsers(RAMSolution):
	minimum = 99999999
	for n in range(1, nNodes):
		if nodes[n][10] == 'computing' and RAMSolution[n] > 0:
			ram = RAMSolution[n]
			if len(nodes[n][11]) <= 3:
				for t in range(nTask):
					if tasks[t][7] == nodes[n][11]:
						ram = ram - tasks[t][1]
			if ram > 0:
					relation = round(nodes[n][4]/ram)
					if relation < minimum:
						minimum = relation
	return minimum


#configuring the policy (user node)
for x in range(nUsers):
	nodes[x][5] = 1

#configuring the policy (rest of nodes). All nodes has been configured with the same node weighting (1)
for x in range(nUsers, nNodes):
	nodes[x][5] = 1


timeBefore = time.time()

opt = Optimize()

opt.minimize(communicationCost + computationCost)		

opt.add([Sum([If(assignment [t][m] ,1,0) for m in range(nNodes)]) == 1 for t in range(nTask*nUsers)])
for t in range(nTask):
	opt.add(Sum([If(assignment [t][node] ,  ((tasks[t][7] == 'none') + (tasks[t][7] == nodes[node][11])),1) for node in range(nNodes)]) == nNodes)


#RAM assignment for each node and user
for u in range(0, nUsers):
	opt.add([Sum([assignment[t+nTask*u][m]*tasks[t+nTask*u][1] for t in range(nTask)]) <= nodes[m][4] for m in range(nNodes)])

#time restrictions
for c in range(0, nConstraints):
	opt.add([(Sum([simplify(assignment[constraints[c][i]+(u*nTask)][m]*If(assignment[constraints[c][j]+(u*nTask)][m],0,1)*relation[constraints[c][i]][constraints[c][j]]*1000000/nodes[m][1])for j in range(2, 2 + constraints[c][1])]) + (assignment[constraints[c][i]+(u*nTask)][m]*tasks[constraints[c][i]+(u*nTask)][0]/nodes[m][0]))*1000000 <= constraints[c][0]*1000000 for i in range(2, 2 + constraints[c][1])  for m in range(nNodes) for u in range(nUsers)])

# if 'energy' in Objectives:
opt.add(communicationCost == Sum([Sum([Sum([Sum([simplify(assignment[i + u*nTask][m]*If(assignment[j+ u*nTask][m],0,1)*(nodes[m][2]*(relation[i][j]/nodes[m][1])*nodes[m][5])) for j in range(nTask)]) for i in range(nTask)]) for u in range(nUsers)]) for m in range(nNodes)]))
opt.add(computationCost == Sum([Sum([simplify(assignment[i][m] * nodes[m][3] * tasks[i][0] * (nodes[m][0]**2) *nodes[m][5]) for i in range(nTask*nUsers)]) for m in range(nNodes)]))

sat = opt.check()
m = opt.model()
timeAfter = time.time()

print('*** Execution finished ***')
print(sat)
if str(sat) == 'sat':
	for t in range (nTask):
		for n in range (nNodes):
			if str(m[assignment[t][n]]) == 'True':
				print('Task ' + str(t) + ' assigned to device ' + str(n))


print('Time required: ' + str(timeAfter - timeBefore))
