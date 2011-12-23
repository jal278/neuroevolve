from nn import *

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def color_disable():
   bcolors.HEADER = ''
   bcolors.BLUE = ''
   bcolors.GREEN = ''
   bcolors.WARNING = ''
   bcolors.RED = ''
   bcolors.ENDC = ''

test_map="""
XXXXXXXXXXXXXXXXXXXXXXXX
X                      X  
X                      X  
X                      X  
X                     XX  
X                      XXXXX   
X             X            XXXXXXXXX
X             X            X      X
X             X      X            X
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XX
                              X    XXXXXX
                              X         X
                              XXXXXXXX  X
                                     X  X
                                     X  X
                                     X +X
                                     XXXX
"""

class map_world:
 def __init__(self,map):
  self.map=map.split("\n")[1:-1]
  self.dist=0
  self.rx=1
  self.ry=1
  self.heading=2
  self.orientations=[(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1)]
  self.sensors=[-2,-1,0,1,2] 
  self.symbol=["-","\\","|","/","-","\\","|","/"]
  self.gx=0
  self.gy=0
  self.score=100000.0
  self.speed=0
  for y in range(len(self.map)):
   for x in range(len(self.map[y])):
    if self.map[y][x]=="+":
     self.gx=x 
     self.gy=y  

 def run_step(self,brain,step):
  brain.load_inputs(self.get_sensors()+[1])
  brain.activate()
  brain.activate()
  outputs=brain.get_outputs()
  mxout = max(outputs)
  if(outputs[1]==mxout):
   self.move()
  elif(outputs[0]==mxout):
   self.turn(-1)
  else:
   self.turn(1)
  dist = (self.rx-self.gx)**2+(self.ry-self.gy)**2
  self.score=min(self.score,dist)
  if(self.score==1 and self.speed==0):
   self.speed=step

 def turn(self,offset):
  self.heading+=offset 

 def move(self):
  self.heading=self.heading % len(self.orientations)
  dx,dy=self.orientations[self.heading]
  nx=self.rx+dx
  ny=self.ry+dy
  if(self.map[ny][nx]==" "):
   self.rx=nx
   self.ry=ny
   self.dist+=1

 def render(self):
  new_map = []
  for k in self.map:
   row=[]
   for c in k:
    if(c=="X"):
     c=bcolors.BLUE+"X"+bcolors.ENDC
    row.append(c)
   new_map.append(row)

  new_map[self.ry][self.rx]=bcolors.RED+self.symbol[self.heading%len(self.symbol)]+bcolors.ENDC

  sensors = self.get_sensors_raw()
  for k in range(len(sensors)):
   orientation=(self.heading+self.sensors[k])%len(self.orientations)
   dx,dy=self.orientations[orientation]
   sx=self.rx+dx
   sy=self.ry+dy
   for z in range(1,sensors[k]):
    new_map[sy][sx]=bcolors.GREEN+"*"+bcolors.ENDC
    sx+=dx
    sy+=dy

  rendered="\n".join(["".join(k) for k in new_map])
  rendered+="\n"
  for k in range(len(sensors)):
   rendered+="Sensor %d:" % k
   bars=bcolors.BLUE+"+"*sensors[k]+bcolors.ENDC+"\n"
   rendered+=bars
  return rendered

 def get_sensors(self):
  return [k/5.0 for k in self.get_sensors_raw()]

 def get_sensors_raw(self):
  sensors=[]
  for k in self.sensors:
   dx,dy=self.orientations[(self.heading+k)%len(self.orientations)]
   sx,sy=self.rx,self.ry
   dist=0
   while(dist<5):
    if(self.map[sy][sx]!=" "):
     break
    dist+=1
    sx+=dx
    sy+=dy
   sensors.append(dist)
  return sensors

def map_evaluate(genome,render=False):
 brain = genome.make_brain()
 brain.clear()
 world=map_world(test_map)
 for k in xrange(300):
  world.run_step(brain,k)
  if(render):
   os.system("clear")
   print world.render()
   print "Timestep: ", k
   time.sleep(0.1)
 score=2000-world.score
 if(world.speed!=0):
  score+=(300-world.speed)*10 
 return score

fname=sys.argv[2]

replay=False
if(sys.argv[1]=="load"):
 replay=True

if(replay):
 a=open(fname,"r")
 best=pickle.load(a)
 map_evaluate(best,True)
else: 
 population=[]
 for k in range(300):
  population.append(dna(6,3))

 best = run_ga(population,map_evaluate,200)
 a=open(fname,"w")
 pickle.dump(best,a)
