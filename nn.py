# simple ANN class
# Joel Lehman

import random
import time
import os
import pickle
import sys

class brain:
 def __init__(self):
  self.nodes=[]
  self.connections=[]
  self.inputs=[]
  self.outputs=[]
 def load_inputs(self,inp):
  num_inp = len(inp)
  for k in range(num_inp):
   self.inputs[k].output=inp[k]
 def get_outputs(self):
  return [k.output for k in self.outputs]
 def activate(self):
  self.clear()
  [k.activate() for k in self.connections]
  [k.activate() for k in self.nodes]
 def clear(self):
  [k.clear() for k in self.nodes]

class connection:
 def __init__(self,from_node,to_node,strength):
  self.from_node=from_node
  self.to_node=to_node
  self.strength=strength
 def activate(self):
  self.to_node.activation+=self.from_node.output*self.strength

#simple threshold unit for now
class node:
 INPUT=0
 OUTPUT=1
 HIDDEN=2
 def __init__(self,type):
  self.type=type
  self.activation=0.0
  self.output=0.0
 def clear(self):
  self.activation=0.0
 def activate(self):
  if(self.type==node.INPUT):
   return
  if(self.activation>2.0):
   self.output=1.0
  elif(self.activation<-2.0):
   self.output=0.0
  else:
   self.output=(self.activation+2.0)/4.0

class dna:
 def __init__(self,inps,outs):
  self.inps=inps
  self.outs=outs
  self.nodes=[node.INPUT]*inps+[node.OUTPUT]*outs
  self.connections=[]
  self.fitness=0
  for k in range(inps):
   for l in range(inps,inps+outs):
    self.connections.append([k,l,random.uniform(-3,3)])

 def copy(self):
  newdna=dna(self.inps,self.outs)
  newdna.nodes=self.nodes[:]
  newdna.connections=[]
  for k in self.connections:
   newdna.connections.append(k[:])
  return newdna

 def mutate(self):
  if random.random()<0.6:
   for k in xrange(random.randint(1,3)):
    self.mutate_connection()
  if random.random()<0.1:
   self.add_connection()
  if random.random()<0.05:
   self.add_node()

 def mutate_connection(self):
  to_mutate = random.choice(self.connections)
  new_strength = to_mutate[2]+random.uniform(-0.5,0.5)
  new_strength = min(3.0,max(-3.0,new_strength))
  to_mutate[2]=new_strength

 def add_connection(self):
  tries = 10
  found=False
  x,y = (None,None)
  while(not found and tries>10):
   found=True
   x = random.choice(range(len(self.nodes)))
   y = random.choice(range(self.inps,len(self.nodes)))
   for k in self.connections:
    if (k[0]==x and k[1]==y):
     tries-=1
     found=False

  if(found):
   self.connections.append([x,y,random.uniform(-1.0,1.0)])

 def add_node(self):
  x=random.randrange(len(self.nodes))
  y=random.randrange(self.inps,len(self.nodes))
  if x==y:
   return

  #add node
  self.nodes.append(node.HIDDEN)
  new_node = len(self.nodes)-1
  #connect node
  #one connection into
  self.connections.append([x,new_node,random.uniform(-3.0,3.0)]) 
  #one connection out (with lower strength to minimize effect on network)
  self.connections.append([new_node,y,random.uniform(-0.5,0.5)])

 def make_brain(self):
  new_brain = brain()
  for k in self.nodes:
   new_node=node(k)
   new_brain.nodes.append(new_node)
   if k==node.INPUT:
    new_brain.inputs.append(new_node)
   elif k==node.OUTPUT:
    new_brain.outputs.append(new_node)

  for k in self.connections:
   from_node=new_brain.nodes[k[0]]
   to_node=new_brain.nodes[k[1]]
   strength=k[2]
   new_brain.connections.append(connection(from_node,to_node,strength))
  return new_brain

def run_ga(population,eval_func,generations):
  best_fit=0
  best=None
  psize=len(population)
  half_psize=psize/2

  for gen in range(generations):
   for k in population:
    k.fitness=eval_func(k)
   
   population.sort(key=lambda k:k.fitness)
   fit = population[-1].fitness
   best = population[-1]
   if(fit>best_fit):
    a=open("best.dat","w")
    pickle.dump(best,a)
    a.close()
    best_fit=fit
    print len(best.connections),len(best.nodes)
   
   print "Generation %d BestFit: %0.3f" % (gen+1,best_fit)
   for k in range(half_psize):
    population[k]=population[k+half_psize].copy()

   for k in population:
    if(k!=best):
     k.mutate()
  return best

def dummy_eval(genome):
 return sum([k[2] for k in genome.connections])

def classify_eval(genome):
 examples = [([0,0],1),([0,1],0),([1,0],0),([1,1],1)]
 brain = genome.make_brain()
 error = 0
 for k in examples:
  brain.clear()
  brain.load_inputs(k[0]+[1])
  brain.activate()
  brain.activate()
  brain.activate()
  error+= (brain.get_outputs()[0]-k[1])**2
 return 100-error
