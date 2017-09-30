# -*- coding: utf-8 -*-
"""
AI Junkie

Genetic algorithm #1

Given the digits 0 through 9 and the operators +, -, * and /,  find a sequence that will represent a given target number. 
The operators will be applied sequentially from left to right as you read.

0:         0000
1:         0001
2:         0010
3:         0011
4:         0100
5:         0101
6:         0110
7:         0111
8:         1000
9:         1001
+:         1010
-:          1011
*:          1100
/:          1101

"""


import random
from numpy.random import choice


D = {10: '+', 11:'-', 12:'*', 13:'/'}
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.001
GENE_LENGTH = 4
CHROMOSOME_LENGTH = 300
POP_SIZE = 100
MAX_GEN = 900

class Chromosome(object):
    def __init__(self):
        self.fScore = 0.0
        self.chromosome = ''

        

##  Convert the chromosome parts into decimal values for easier handling.
##
def BinToDec(string):
    val = 0
    add = 1
    for i in string[::-1]:
        if i == '1':
            val += add
        add *= 2
    return val

##  Parse the chromosome into GENE_LENGTH segments of operator - number pairs
##

def parser(chromosome):   
    chromosome = chromosome[:(len(chromosome)//GENE_LENGTH)*GENE_LENGTH]
    bits = [chromosome[i:i+GENE_LENGTH] for i in range(0, len(chromosome), GENE_LENGTH)]
    bits = bits[:CHROMOSOME_LENGTH-1]
    seq = []
    bOperator = False
    for bit in bits:
        b = BinToDec(bit)
        if bOperator:
            if b < 10 or b > 13:
                continue
            else:
                seq.append(b)
                bOperator = False
        else:
            if b > 9:
                continue
            else:
                seq.append(b)
                bOperator = True
    for i in range(len(seq)-1):
        if seq[i] == 13 and seq[i+1] == 0:
            seq[i] = 10
    if seq[-1] in range(10, 14):
        seq = seq[:-1]
    return seq

def fScore(chromosome, target):
    seq = parser(chromosome)
    val = seq[0]
    for i in range(1, len(seq), 2):
        if seq[i] == 10:
            val += seq[i+1]
        elif seq[i] == 11:
            val -= seq[i+1]
        elif seq[i] == 12:
            val *= seq[i+1]
        else:
            val /= seq[i+1]
    if val == target:
        return 1237
    else:
        return abs(1/(val-target))

def randomizeChromosome(length):
    res = ''
    for i in range(length):
        if random.random() > 0.5:
            res += '1'
        else:
            res += '0'
    return res

def printChromosome(chromosome):
    seq = parser(chromosome)
    res = ''
    for v in seq:
        if v < 10:
            res += str(v)
        elif v > 9 and v < 14:
            res+=  ' ' + D[v] + ' '
    print(res)
    return
    
def drawChromosome(totalFitness, population):
    pDistribution = [c.fScore/totalFitness for c in population]
    draw = choice(population, 1, p=pDistribution, replace=False)
    return draw[0].chromosome
    
def crossover(chr1, chr2):
    if random.random() > CROSSOVER_RATE:
        point = int(random.random()*10)
        temp = chr1
        chr1 = chr1[:point] + chr2[point:]
        chr2 = chr2[:point] + temp[point:]
    return chr1, chr2


def mutate(chromosome):
    res = ''
    for bit in chromosome:
        if random.random() < MUTATION_RATE:
            if bit == '1':
                res += '0'
            else:
                res += '1'
        else:
            res += bit
    return res

def geneticAlgorithm(targetValue):
    bFound = False
    gReq = 0
    population = []
    random.seed()
    for i in range(POP_SIZE):
        c = Chromosome()
        c.chromosome = randomizeChromosome(CHROMOSOME_LENGTH)
        population.append(c)
    while not bFound:
        totalFitness = 0.0
        for chromosome in population:
            score = fScore(chromosome.chromosome, targetValue)
            chromosome.fScore = score
            totalFitness += score
        
        for chromosome in population:
            if chromosome.fScore == 1237:
                print("Solution found in %d generations." % gReq)
                printChromosome(chromosome.chromosome)
                bFound = True
                return
            
        newPopulation = []
        while len(newPopulation) != POP_SIZE:
            chr1 = drawChromosome(totalFitness, population)
            chr2 = drawChromosome(totalFitness, population)
            chr1, chr2 = crossover(chr1, chr2)
            chr1 = mutate(chr1)
            chr2 = mutate(chr2)
            c1 = Chromosome()
            c2 = Chromosome()
            c1.chromosome = chr1
            c2.chromosome = chr2
            newPopulation.append(c1)
            newPopulation.append(c2)
        population = newPopulation[:]
        gReq += 1        
        if gReq > MAX_GEN:
            print("Could not find a solution within %d genereations" % MAX_GEN)
            return
            
            
        
        
                



    
    
        
                
        
        
    
    
        
    

