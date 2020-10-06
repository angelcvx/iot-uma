from z3 import *
from random import randint
import random
import time

communicationCost = Real('communicationCost')
communicationCostDown = Real('communicationCostDown')
computationCost = Real('computationCost')
communicationCostUser = Real('communicationCostUser')
communicationDownUser = Real('communicationDownUser')
computationCostUser = Real('computationCostUser')
nTask = 10
nNodes = 12
nUsers = 1
nConstraints = 2
nMeshlium = 6
batteryLevel = randint(0,100)

#{task, node}
assignment = [ [ Bool("ASING_%s_%s" % (r,c)) for c in range(nNodes+nUsers-1) ] 
      for r in range(nTask*nUsers) ]

#{node, user}
RAMresources = [ [ Real("RAM_%s_%s" % (r,c)) for c in range(nUsers+nUsers-1) ] 
for r in range(nNodes) ]


#data to be transmitted between tasks
relation = [ [ 0 for c in range(nTask) ] 
      for r in range(nTask) ]

relation[1][2] = 30/8
relation[2][3] = 8806/8
relation[3][4] = 3000/8
relation[4][5] = 150/8
relation[5][6] = 155/8
relation[7][8] = 50/8
relation[6][9] = 25/8
relation[8][9] = 25/8

tasks = [ [ 0 for c in range(3) ] 
      for r in range(nTask*nUsers) ]

#{CPU, RAM, user}
aux = 0
for x in range(0, nUsers):
	tasks[aux][0] = 3000 #CameraCalibration
	tasks[aux][1] = 10
	tasks[aux][2] = x
	tasks[aux+1][0] = 200 #RequestFrame
	tasks[aux+1][1] = 5
	tasks[aux+1][2] = x
	tasks[aux+2][0] = 4000 #CaptureFrame
	tasks[aux+2][1] = 15
	tasks[aux+2][2] = x
	tasks[aux+3][0] = 550000000 #getFeatures
	tasks[aux+3][1] = 70
	tasks[aux+3][2] = x
	tasks[aux+4][0] = 400000000 #detectMarker
	tasks[aux+4][1] = 70
	tasks[aux+4][2] = x
	tasks[aux+5][0] = 500000000 #identifyMarker
	tasks[aux+5][1] = 70
	tasks[aux+5][2] = x
	tasks[aux+6][0] = 200 #getMarkerInfo
	tasks[aux+6][1] = 5
	tasks[aux+6][2] = x
	tasks[aux+7][0] = 30000 #getGPS
	tasks[aux+7][1] = 10
	tasks[aux+7][2] = x
	tasks[aux+8][0] = 300 #consultObjectsInPosition
	tasks[aux+8][1] = 15
	tasks[aux+8][2] = x
	tasks[aux+9][0] = 40000 #overlayContent
	tasks[aux+9][1] = 100
	tasks[aux+9][2] = x
	aux = aux + nTask


constraints = [ [ 0 for c in range(nTask) ] 
      for r in range(nConstraints) ]

#[0] max time to be executed
#[1] number of tasks involved in the restriction
#[2...n] index of the involved tasks
constraints[0][0] = 0.034
constraints[0][1] = 8
constraints[0][2] = 0
constraints[0][3] = 1
constraints[0][4] = 2
constraints[0][5] = 3
constraints[0][6] = 4
constraints[0][7] = 5
constraints[0][8] = 6
constraints[0][9] = 9
constraints[1][0] = 0.034
constraints[1][1] = 4
constraints[1][2] = 3
constraints[1][3] = 7
constraints[1][4] = 8
constraints[1][4] = 9

nodes = [ [ 0 for c in range(8) ] 
      for r in range(nNodes+nUsers-1) ]

#{CPU, Bandwidth. Power Upload, k, RAM, policy, Power Download, BandwidthDown}
for x in range(0, nUsers):
	nodes[x][0] = random.uniform(160000000,2400000000)
	nodes[x][1] = random.uniform(100000000,150000000)
	nodes[x][2] = random.uniform(1,1.5)
	nodes[x][3] = random.uniform(0.00000000001,0.000000001)
	nodes[x][4] = random.uniform(3000,4000)
	nodes[x][5] = 1
	nodes[x][6] = random.uniform(1,1.5)
	nodes[x][7] = random.uniform(3000000,4000000)

for x in range(1, nMeshlium +1):
	nodes[x][0] = random.uniform(100000000,1600000000)
	nodes[x][1] = random.uniform(5000000,15000000)
	nodes[x][2] = random.uniform(1,1.5)
	nodes[x][3] = random.uniform(0.00000000001,0.000000001)
	nodes[x][4] = random.uniform(3000,4000)
	nodes[x][6] = random.uniform(1,1.5)
	nodes[x][7] = random.uniform(3000000,4000000)



#Cloud Server
nodes[nUsers + nMeshlium][0] = random.uniform(2400000000,3600000000)
nodes[nUsers + nMeshlium][1] = random.uniform(700000,1000000)
nodes[nUsers + nMeshlium][2] = random.uniform(1,1.5)
nodes[nUsers + nMeshlium][3] = random.uniform(0.00000000001,0.000000001)
nodes[nUsers + nMeshlium][4] = random.uniform(28000,32000)
nodes[nUsers + nMeshlium][6] = random.uniform(1,1.5)
nodes[nUsers + nMeshlium][7] = random.uniform(700000,1000000)

#Server Internal
nodes[nUsers + nMeshlium + 1][0] = random.uniform(1200000000,1800000000)
nodes[nUsers + nMeshlium + 1][1] = random.uniform(100000000,150000000)
nodes[nUsers + nMeshlium + 1][2] = random.uniform(1,1.5)
nodes[nUsers + nMeshlium + 1][3] = random.uniform(0.00000000001,0.000000001)
nodes[nUsers + nMeshlium + 1][4] = random.uniform(6000,8000)
nodes[nUsers + nMeshlium + 1][6] = random.uniform(1,1.5)
nodes[nUsers + nMeshlium + 1][7] = random.uniform(3000000,4000000)

#Computer 1
for x in range(nMeshlium + 2, nMeshlium +5):
	nodes[nUsers + x][0] = random.uniform(1000000000,150000000)
	nodes[nUsers + x][1] = random.uniform(100000000,150000000)
	nodes[nUsers + x][2] = random.uniform(1,1.5)
	nodes[nUsers + x][3] = random.uniform(0.00000000001,0.000000001)
	nodes[nUsers + x][4] = random.uniform(6000,8000)
	nodes[nUsers + x][6] = random.uniform(1,1.5)
	nodes[nUsers + x][7] = random.uniform(3000000,4000000)

# Fixed amount of RAM for nodes (2Gb)
for x in range(nNodes):
	nodes[x][4] = 2000

#configuring the policy (user node)
for x in range(nUsers):
	nodes[x][5] = 1

#configuring the policy (rest of nodes). All nodes has been configured with the same node weighting (1)
for x in range(nUsers, nNodes):
	nodes[x][5] = 1


timeBefore = time.time()

opt = Optimize()

opt.add([Sum([If(assignment [t][m] ,1,0) for m in range(nNodes)]) == 1 for t in range(nTask*nUsers)])
opt.add([Sum([If(RAMresources [m][u] >= 0,1,0) for u in range(nUsers)]) == nUsers for m in range(nNodes)])
opt.add([Sum([RAMresources [m][u] for u in range(nUsers)]) <= nodes[m][4] for m in range(nNodes)])

#tasks t1,t3 t8 and t10 are assigned to the user's node
opt.add(Sum([If(assignment [0 + nTask*u][u],1,0)* If(assignment [2 + nTask*u][u],1,0) * If(assignment [7 + nTask*u][u],1,0) * If(assignment [9 + nTask*u][u],1,0)  for u in range(nUsers)]) == nUsers)

#RAM assignment for each node and user
for u in range(0, nUsers):
	opt.add([Sum([assignment[t+nTask*u][m]*tasks[t+nTask*u][1] for t in range(nTask)]) <= RAMresources[m][u] for m in range(nNodes)])

#time restrictions
for c in range(0, nConstraints):
	opt.add([(Sum([simplify(assignment[constraints[c][i]+(u*nTask)][m]*If(assignment[constraints[c][j]+(u*nTask)][m],0,1)*relation[constraints[c][i]][constraints[c][j]]*1000000/nodes[m][1])for j in range(2, 2 + constraints[c][1])]) + (assignment[constraints[c][i]+(u*nTask)][m]*tasks[constraints[c][i]+(u*nTask)][0]/nodes[m][0]))*1000000 <= constraints[c][0]*1000000 for i in range(2, 2 + constraints[c][1])  for m in range(nNodes) for u in range(nUsers)])

opt.add(communicationCost == Sum([Sum([Sum([Sum([simplify(assignment[i + u*nTask][m]*If(assignment[j+ u*nTask][m],0,1)*(nodes[m][2]*(relation[i][j]/nodes[m][1])*nodes[m][5])) for j in range(nTask)]) for i in range(nTask)]) for u in range(nUsers)]) for m in range(nNodes)]))
opt.add(computationCost == Sum([Sum([simplify(assignment[i][m] * nodes[m][3] * tasks[i][0] * (nodes[m][0]**2) *nodes[m][5]) for i in range(nTask*nUsers)]) for m in range(nNodes)]))
opt.add(communicationCostDown == Sum([Sum([Sum([Sum([simplify(assignment[i + u*nTask][m]*If(assignment[j+ u*nTask][m],0,1)*(nodes[m][6]*(relation[j][i]/nodes[m][7])*nodes[m][5])) for j in range(nTask)]) for i in range(nTask)]) for u in range(nUsers)]) for m in range(nNodes)]) )
opt.minimize(communicationCost + communicationCostDown + computationCost)

opt.add(communicationCostUser == Sum([Sum([Sum([simplify(assignment[i + u*nTask][0]*If(assignment[j+ u*nTask][0],0,1)*(nodes[0][2]*nodes[0][5]*(relation[i][j]/nodes[0][1]))) for j in range(nTask)]) for i in range(nTask)]) for u in range(0,nUsers)]))
opt.add(communicationDownUser == Sum([Sum([Sum([simplify(assignment[i + u*nTask][0]*If(assignment[j+ u*nTask][0],0,1)*(nodes[0][6]*nodes[0][5]*(relation[j][i]/nodes[0][7]))) for j in range(nTask)]) for i in range(nTask)]) for u in range(0,nUsers)]))
opt.add(computationCostUser == Sum(Sum([simplify(assignment[i][0] * nodes[0][3] * tasks[i][0] * (nodes[0][0]**2) *nodes[0][5]) for i in range(nTask*nUsers)])))

print(opt.check())
m = opt.model()
timeAfter = time.time()

# for d in m:
# 	print(m)

# print()
# print (sorted ([(d, m[d]) for d in m], key = lambda x: str(x[0])))
for t in range (nTask):
	for n in range (nNodes):
		if str(m[assignment[t][n]]) == 'True':
			print('Task ' + str(t) + ' assigned to device ' + str(n))
print('\n')
print('Energy consumption in the DI: ' + str(m[computationCost].numerator_as_long()/m[computationCost].denominator_as_long() + m[communicationCost].numerator_as_long()/m[communicationCost].denominator_as_long() + m[communicationCostDown].numerator_as_long()/m[communicationCostDown].denominator_as_long() - m[computationCostUser].numerator_as_long()/m[computationCostUser].denominator_as_long() - m[communicationCostUser].numerator_as_long()/m[communicationCostUser].denominator_as_long()) + ' (J)')
print('Energy consumption in the user node: ' + str(m[computationCostUser].numerator_as_long()/m[computationCostUser].denominator_as_long() + m[communicationCostUser].numerator_as_long()/m[communicationCostUser].denominator_as_long() +  m[communicationDownUser].numerator_as_long()/m[communicationDownUser].denominator_as_long()) + ' (J)')
totalTime = timeAfter - timeBefore
print('Execution time: ' + str(totalTime) + ' (s)')