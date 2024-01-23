import random, time

regular, splatfest, closeout = 1, 1.2, 1.5
multipliers = [regular, splatfest, closeout]

#need to make a thing for anarchy battle rules

###################      0-1
multiplier = multipliers[0]
levelsNeeded = 100#-77
####################

def percentage(part, whole):
  Percentage = 100 * float(part)/float(whole)
  return int(Percentage)

def calculate(returnBool=False, levelsNeeded=levelsNeeded, multiplier=multiplier, chance=[42,42,16]):#always equels 100
    total=0
    rounds=0
    disconnect, lose, win = 0, 800*multiplier, 1400*multiplier
    disconnects, losses, wins = 0, 0, 0
    chanceTotal = chance[0] + chance[1] + chance[2]#should get accurate 100%
    winPercent = percentage(chance[0], chanceTotal)
    losePercent = percentage(chance[1], chanceTotal)
    disconnectPercent = percentage(chance[2], chanceTotal)#->100#percentage(chance[2], 100)+winPercent+losePercent
    chancePercent = winPercent+losePercent+disconnectPercent
    #print(f"{chanceTotal}: {winPercent}, {losePercent}, {disconnectPercent}.     {chancePercent}")
    winRange = []
    loseRange = []
    disconnectRange = []
    for i in range(100):
        if winPercent > 0: 
            winRange.append(i+1)
            winPercent -= 1
        elif losePercent > 0:
            loseRange.append(i+1)
            losePercent -= 1
        elif disconnectPercent > 0:
            disconnectRange.append(i+1)
            disconnectPercent -= 1
    #print(f"{chanceTotal}: {winPercent}, {losePercent}, {disconnectPercent}.     {chancePercent}")
    
    battletime,lobbytime = 3, 2
    timeperround = battletime + lobbytime
    while True:
        toss = random.randint(1,100)#1-12
        rounds += 1
        if toss in disconnectRange:#11
            total += disconnect
            disconnects += 1
            
        elif toss in loseRange:#6
            total += lose
            losses += 1
        elif toss in winRange:#1#doesn't need percentvalue
            total += win
            wins += 1
        if len(disconnectRange) == 100: 
            disconnects = 3.14159265
            total = 9500*levelsNeeded+9
        if total > 9500*levelsNeeded: break
    if not returnBool == True:
        print(f"Lvl {100-levelsNeeded}->100,  +{'{:,}'.format(int(total))}p in  {int(float(str(timeperround*rounds/60)[:5]))}H   {rounds}:  {wins}W  {losses}L  {disconnects}D  x{multiplier}")
        time.sleep(1)
        total=0
        rounds=0
        disconnect, lose, win = 0, 800*multiplier, 1400*multiplier
        disconnects, losses, wins = 0, 0, 0
    if returnBool == True:
        return 100-levelsNeeded, f"+{'{:,}'.format(int(total))}p", int(float(str(timeperround*rounds/60)[:5])), rounds, wins, losses, disconnects, multiplier
    

#while True:
#    calculate()