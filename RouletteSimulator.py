#Roulette Simulation

#Board
# |36|912|1518|2124|2730|3336
#0|25|811|1417|2023|2629|3235
# |14|710|1316|1922|2528|3134

import random
from functools import reduce
#import openpyxl
#import os

#wb = openpyxl.Workbook()

simLength = int(input("How many games or spins do you want to simulate? "))
payout = int(input("What is the coner bet payout (standard is 8 to 1)? "))
money = int(input("How much money are you starting with? "))

def spin(): #This function spins the roulette wheel to generate a random number between 0 and 36
    spin.counter += 1 #This counts the number of spins
    number = random.randint(0,36)
    #nums.append(number)#TAKE THIS OUT FOR FINAL
    return(number)
spin.counter = 0

def betAmount(gameSpin): #This sets the bet amount for each square
    if(gameSpin == 0): #1 = 4 winning numbers [10.81%]
        return(1) #Betting $1 total - $1.00 per square
    elif(gameSpin == 1): #2 squares = 8 winning numbers (6 if neighboring) [18.92%] +8.11%
        return(2) #Betting $4 total - $1.75 per square (rounded)
    elif(gameSpin == 2): #3 squares = 12 winning numbers (10 if neighboring) [29.73%] +10.81%
        return(3) #Betting $9 total - $2.75 per square (rounded)
    elif(gameSpin == 3): #4 squares = 16 winning numbers (12 or 14 if neighboring) [37.84%] +8.11%
        return(4) #Betting $16 total - $3.50 per square (rounded)
    elif(gameSpin == 4): #5 squares = 20 winning numbers (16 or 18 if neighboring) [48.65%] +10.81%
        return(5) #Betting $25 total - $4.50 per square (rounded)
    elif(gameSpin == 5): #6 squares = 24 winning numbers (18, 20, or 22 if neighboring) [56.76%] +8.11%
        return(5) #Betting $30 total - $5.25 per square (rounded)
    elif(gameSpin == 6): #7 squares = 26 winning numbers (22 or 24 if neighboring) [64.87%] +8.11% - This is the peak in difference of probability
        return(6) #Betting $42 total - $6.00 per square
    elif(gameSpin == 7): #8 squares = 28 winning numbers (24 or 26 if neighboring) [70.27%] +5.40%
        return(7) #Betting $56 total - $6.50 per square (rounded)
    elif(gameSpin == 8): #9 squares = 30 winning numbers (28 if neighboring) [78.38%] +8.11%
        return(7) #Betting $63 total - $7.25 per square (rounded)
    elif(gameSpin == 9): #10 squares = 32 winning numbers (30 if neighboring) [83.78%] +5.40%
        return(8) #Betting $80 total - $7.75 per square (rounded)
    elif(gameSpin == 10): #11 squares = 34 winning numbers [91.89%] +8.11%
        return(9) #Betting $99 total - $8.50 per square (rounded)
    elif(gameSpin == 11): #12 squares = 36 winning numbers [THIS IS THE MAX POSSIBLE: 97.30% WIN] +5.40%
        return(9) #Betting $108 total - $9.00 per square
    else:
        return(None)

#This is the betting sets layout. Each bet will be placed so that it applies to a set depending upon the spin. Set 'a' has 0 for inclusivity.
sets = {'a':[1,2,4,5],'aa':[2,3,5,6],'b':[7,8,10,11],'bb':[8,9,11,12],'c':[13,14,16,17],'cc':[14,15,17,18],
        'd':[19,20,22,23],'dd':[20,21,23,24],'e':[25,26,28,29],'ee':[26,27,29,30],'f':[31,32,34,35],'ff':[32,33,35,36]}

lst = []
def bet(nums,zero):
    #For every number in the list, place a single bet (on the square corner)
    #Activate each of the four numbers on the board for each square
    lst.clear() #This clears the winning numbers list to avoid duplicates
    winners.clear() #This clears the winning numbers list to avoid duplicates
    for i in nums: #For every previous spin number
        counter = 0
        if(i == 0 and zero == 0):
            lst.append(sets['a'])
            zero += 1
        for ii in sets: #And for every number in the sets of corner bet squares
            if(i in sets[ii]): #If the number is in a set that hasn't won, add that set to the winning numbers list for betting
                if(counter == 0):
                    lst.append(sets[ii])
                    counter += 1 #This avoids double betting for middle numbers (overlapping sets)

winners = []
def flatten(lst): #Converts the nested list of winning bets "lst" into a flat list "winners"
    for i in lst: 
        if type(i) == list: 
            flatten(i) 
        else: 
            winners.append(i) 

nums = [] #The numbers in the previous spins
zero = 0
game = 0 #A set of spins between each win
gameSpin = 0 #The number of spins within each game between wins
balance = [] #The monetary balance over time per spin
while(spin.counter <= simLength-1 and money >= 0):
    if(game == 0): #Starting game: Bet on 1,2,4,5 since the previous spin isn't known
        if(gameSpin == 0): #Assume the previous spin was 1 if it's the first spin to be played
            nums.append(1)
        bet(nums,zero) #Make the bet
        money = money - betAmount(gameSpin)*len(nums) #Bets on the table
        balance.append(money) #Log the bet
        flatten(lst) #Determine which numbers will be winners
        if(money <= 0): #If everything is lost, then don't go into debt
            break
        num = spin() #Spin the roulette wheel
        gameSpin += 1 #Mark the spin
        if(num in winners): #If WIN
            #if(num != 0): #0s are a loss
                hit = winners.count(num) #The number of bets that get hit by the spin number (should only be 1 or 2)
                money = money + betAmount(gameSpin-1)*payout*hit + betAmount(gameSpin-1)*hit #Get paid!
                #money = original amount after placing bet + amount bet * payout * number of bets that won + amount bet * amount of bets that won
                balance.append(money) #Log the winnings
                nums.clear() #Reset the spin numbers list
                game += 1 #Start a new game
                gameSpin = 0 #Reset the game spin count
                zero = 0
        elif(gameSpin == 7): #If TOO MANY SPINS: Getting too pricy
            #money = money - betAmount(gameSpin-1)*len(nums) #Lose our bets
            #balance.append(money)
            nums.clear() #Reset the spin numbers list
            game += 1 #Start a new game
            gameSpin = 0 #Reset the game spin count
            zero = 0
        nums.append(num) #Add the spin numbers to the list

    else: #Each game proceeds after the last with the initial bet landing on the ending spin of the previous game
        bet(nums,zero) #Make the bet
        money = money - betAmount(gameSpin)*len(nums) #Bets on the table
        balance.append(money) #Log the bet
        flatten(lst) #Determine which numbers will be winners
        if(money <= 0): #If everything is lost, then don't go into debt
            break
        num = spin() #Spin the roulette wheel
        gameSpin += 1 #Mark the spin
        if(num in winners): #If WIN
            #if(num != 0): #0s are a loss
                hit = winners.count(num) #The number of bets that get hit by the spin number (should only be 1 or 2)
                money = money + betAmount(gameSpin-1)*payout*hit + betAmount(gameSpin-1)*hit #Get paid!
                #money = original amount after placing bet + amount bet * payout * number of bets that won + amount bet * amount of bets that won
                balance.append(money) #Log the winnings
                nums.clear() #Reset the spin numbers list
                game += 1 #Start a new game
                gameSpin = 0 #Reset the game spin count
                zero = 0
        elif(gameSpin == 7): #If TOO MANY SPINS: Getting too pricy
            #money = money - betAmount(gameSpin-1)*len(nums) #Lose our bets
            #balance.append(money)
            nums.clear() #Reset the spin numbers list
            game += 1 #Start a new game
            gameSpin = 0 #Reset the game spin count
            zero = 0
        nums.append(num) #Add the spin numbers to the list

#os.chdir('C:\\Users\\Jared\\Dropbox')
#ws1 = wb.active
#ws1.title = 'Data'
#for row in range(0, len(balance)):
#    wor = balance[row]
#    ws1.append([wor])
#wb.save('Roulette Strategy Monte Carlo Simulation Report.xlsx')
