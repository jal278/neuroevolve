from corridor import *

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
 map_evaluate(best,render=True)
else: 
 population=[]
 for k in range(300):
  population.append(dna(6,3))

 best = run_ga(population,map_evaluate,200)
 a=open(fname,"w")
 pickle.dump(best,a)
