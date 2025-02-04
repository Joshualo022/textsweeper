'''TEXTSWEEPER BY JOSH LO - COMPLETED JAN 6 2022
Console/text based game. Interact with typing
Cheat code for script testing: uuddlrlrba (konami code letters)
YOUR PROGRESS IS SAVED LOCALLY!!!
'''



from math import *
from random import *
from datetime import *

#login

#READS THE LIST OF USERNAMES AND PASSCODES


u = open('user.txt','r')
p = open('codes.txt','r')
userl = u.readlines()
codel = p.readlines()
for i in range(len(userl)):
  userl[i] = userl[i].strip()
for i in range(len(codel)):
  codel[i] = codel[i].strip()

u.close()
p.close()



usernames = open('user.txt','a')
passcodes = open('codes.txt','a')
stats = open('stats.txt','a')

#USER LOGIN DISPLAY AND INPUT
welcomemessage = "\U0001F4A3 WELCOME TO MINESWEEPER V1. \U0001F4A3\n".center(20)

print(welcomemessage)
username = input("Sign in with username. Or create one to start. \n[>]")
if username in userl:
    print('\nlogged in with an existing account: ',username)
    userid = userl.index(username)
    password = input("Enter your passcode: \n[>]")
    while password != codel[userid]:
      password = input("Incorrect password! Enter your passcode: \n[>]")
    print('\nWelcome!',username,'\n')
else:
    print('\nWelcome!',username,'\n')
    password = input("\nCreate your passcode:\n[>]")
    usernames.seek(0,0)
    usernames.write(username + '\n')
    passcodes.seek(0,0)
    passcodes.write(password + '\n')
    stats.seek(0,0)
    stats.write('PLAYER: T0W0H0' + '\n')

    usernames.close()
    passcodes.close()

    u = open('user.txt','r')
    p = open('codes.txt','r')
    userl = u.readlines()
    codel = p.readlines()
    for i in range(len(userl)):
      userl[i] = userl[i].strip()
    for i in range(len(codel)):
      codel[i] = codel[i].strip()

    u.close()
    p.close()

    userid = userl.index(username)
# (T) is the number of games played
# (W) is games Won
# (H) is high score

stats.close()


#LOAD STATS INTO GLOBAL VARIABLES



s = open('stats.txt','r')

stl = s.readlines()

try:
  stt = int(stl[userid][stl[userid].find('T') + 1:stl[userid].find('W')])
except:
  stt = 0
try:
  stw = int(stl[userid][stl[userid].find('W') + 1:stl[userid].find('H')])
except:
  stw = 0
try:
  sth = stl[userid][stl[userid].find('H') + 1:]
  sth = sth.strip()
except:
  sth = None






#start

gameover = 0
mines = 15
lettercoords = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']



'''generate dictionary function
Dx = x values of grid, Dy = y values of grid
indict = dictionary to return/change
dominant = does it go by columns or rows?'''

griddict = {}
viewdict = {}
def generatedict(dx,dy,indict,dominant):
    if dominant == 'x':
        for x in dx:
            for y in dy:
                key = x + str(y)
                indict[key] = 'x'
    else:
        for y in dy:
            for x in dx:
                key = x + str(y)
                indict[key] = 'x'

#generate mines function

def addmines(minecount,keys):
    for i in range(minecount):
        randommine = choice(keys)
        if griddict[randommine] == 'M':
            while True:
                randommine = choice(keys)
                if griddict[randommine] != 'M':
                    break
        griddict[randommine]= 'M'

#check for mine function

def checkmine(x,y,returntype):

    hoplistx = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N']
    hoplisty = ['0','1','2','3','4','5','6','7','8','9']
    surroundlist = []
    Checkcoords = x + y
    for h in range(-1,2):
        for k in range(-1,2):
            try:
                hopindex = hoplistx[(hoplistx.index(Checkcoords[0])) + h] + hoplisty[(hoplisty.index(Checkcoords[1])) + k]
                surroundlist.append(hopindex)   
            except:
                surroundlist.append('00') 
    if returntype == 'sumine':
        if griddict[surroundlist[4]] == 'M':
            return 'game'

    sumine = 0
    removeindex = 0
    for i in surroundlist:
        if '0' in i:
            surroundlist[removeindex] = 'tbr'
        elif griddict[i] == 'M':
            sumine += 1
        removeindex += 1

    for i in surroundlist:
        try:
            surroundlist.remove('tbr')
        except:
            pass   
    if sumine == 0:
        sumine = ' '

    if returntype == 'sumine':
        return sumine
    else:
        return surroundlist

'''def addscore(userid,scorelocal):
  if username in scoresdict:
    if scorelocal > scoresdict[userid]:
      scoresdict[userid] = scorelocal
  else:
    scoresdict[userid] = scorelocal '''

def printgrid(grid):
        print('\n')
        print('/   ', end='')
        for i in lettercoords:
            print(i,end = '  ')
        print('\\\n')

        printindex = 20 
        yvalue = 1
        for i in grid.keys():

            if printindex == 20:
                printindex = 0
                print(yvalue,end = '   ')
                yvalue += 1
                print(grid[i],end = '  ')
                printindex += 1
            elif printindex < 13:
                print(grid[i],end = '  ')
                printindex += 1
            else:
                print(grid[i],end = '\n')
                printindex = 0
                if yvalue < 10:
                    print(yvalue,end = '   ')
                    yvalue += 1
                else:
                    print('\n\\   \U0001F4A3   There are',minesleft,'mines remaining   \U0001F4A3   /')



#Beginning game loop, generates the grid goes back here when round ends.


while True:
    #if username in scoresdict:
      #print('your high score is',scoresdict[username])

    print('|____________________________\U0001F4A3\n|PLAYER PROFILE:[',username,']\n|GAMES PLAYED: ',stt,'\n|GAMES WON:    ',stw,'\n|FASTEST TIME: ',sth,'\n|___________________________\U0001F4A3\n')

    gamestart = datetime.today()
    turn = 1
    minesleft = mines

    generatedict(lettercoords,[1,2,3,4,5,6,7,8,9],griddict,'x')
    generatedict(lettercoords,[1,2,3,4,5,6,7,8,9],viewdict,'y')

    addmines(mines, list(griddict.keys()))
    print('You stepped on a minefield, there are 15 mines. \nFind them all!')

    #In game , game loop. Makes up code for one round.

    while gameover == 0:

        print('============================================\n================= TURN',turn,'===================\n============================================')
        printgrid(viewdict)

        #ACTION INPUT AND CHECK

        action = str(input('\n\U0001F916 Type a Coordinate to uncover - \nex:"J7" or M to mark a mine\n[>]'))
        if action.upper() == 'UUDDLRLRBA':
          gameover = 2
        if action.upper() == 'M':
            mark = str(input('\n\U0001F916 MARK OR UNMARK MINE! Watch out, the counter will go down even if you marked wrong!\n[>]'))
            mark = mark.upper()
            try:
                if viewdict[mark] == 'x':
                    viewdict[mark] = '?'
                    print(mark,'LAST MOVE: WAS MARKED AS A MINE. The counter goes down by 1...')
                    minesleft -= 1
                elif viewdict[mark] == '?':
                    viewdict[mark] = 'x'
                    print(mark,'LAST MOVE: WAS UNMARKED. The counter goes up by 1...')
                    minesleft += 1
                elif viewdict[mark].isdigit():
                    print('LAST MOVE: Block already uncovered')
            except:
                print('LAST MOVE: Coordinate not found')
        elif action.upper() in list(griddict.keys()):
            action = action[0].upper() + action[1]

            if checkmine(action[0].upper(),str(action[1]),'sumine') == 'game':
                viewdict[action] = '\U0001F4A3'
                for i in griddict.keys():
                    if griddict[i] == 'M':
                        viewdict[i] = '\U0001F4A3'
                gameover = 1
            else:
                print('LAST MOVE: UNCOVERED',action)
                viewdict[action] = checkmine(action[0].upper(),str(action[1]),'sumine')
        else:
            print('LAST MOVE: Invalid Action, try again.')

#ENDROUND CHECKS. CODE THAT IS RUN AFTER EVERY ACTION TO PERFORM SPECIAL ACTIONS.

        #CHECKS FOR SURROUNDING EMPTY SPACES
        def chesurempty():
            for key in viewdict.keys():
                surcheck = checkmine(key[0],str(key[1]),'surroundlist')
                if viewdict[key] == ' ':
                    for coord in surcheck:
                        if checkmine(coord[0].upper(),str(coord[1]),'sumine') != 'game':
                            viewdict[coord] = checkmine(coord[0].upper(),str(coord[1]),'sumine')

        chesurempty()
        chesurempty()
        chesurempty()

        #CHECKS IF WON OR LOST



        if minesleft == 0:
            for i in viewdict.keys():
                if viewdict[i] == 'x':
                    if checkmine(i[0].upper(),str(i[1]),'sumine') == 'game':
                        gameover = 3
                        break
                else:
                    pass

        if minesleft == 0:
            if gameover == 0:
                gameover = 2



        turn += 1

        '''^^^ WILL LOOP BACK HERE UNLESS GAME OVER ^^^
              ______________________________________'''

    stt += 1

    printgrid(viewdict)
    if gameover == 1:
        cont = input('\U0001F4A3\U0001F4A3\U0001F4A3 You stepped on a mine! Play again? [Y,N] or [L] to see the leaderboard.')
    elif gameover == 2:
        stw += 1
        gameend = datetime.today()
        gametime = gameend - gamestart
        for t in range(0,15):
          print('\U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3 \U0001F4A3')
        print('\n==============================\n\U0001F973\U0001F973\U0001F973 AWESOME, YOU MARKED ALL THE MINES! \nYour score(time) is:',gametime, '\n==============================\n')

#DECIDES IF SCORE IS HIGH SCORE
        if sth != '0':
          sthtts = (int(sth[2:4]) * 60) + (int(sth[8:])/10000000) + int(sth[5:7])

        if sth == '0':
          sth = str(gametime)
        elif sthtts >= int(gametime.total_seconds()):
          sth = str(gametime)

#READS AND CHANGES STATS FILE

        newstl = 'PLAYER: T{:s}W{:s}H{:s}'.format(str(stt),str(stw),str(sth))

        stapread = open('stats.txt','r')
        stapl = stapread.readlines()
        stapread.close()

        stap = open('stats.txt','w')
        lineid = 0
        for line in stapl:
          if lineid == userid:
            stapl[lineid] = newstl + '\n'
          lineid += 1

        stap.seek(0)
        for i in stapl:
          stap.write(i)

        stl = newstl
        stap.close()

        cont = input('\U0001F916 Your score is being saved.... Play again? \n[Y,N] or [S] to view your stats.\n\n[>]')

    elif gameover == 3:
        print('==============================\n\U0001F4A3\U0001F4A3\U0001F4A3 OH NO! You marked an incorrect mine! GAME OVER...\n==============================')
        cont = input('\U0001F4A3\U0001F4A3\U0001F4A3 You miscalculated... Play again? [Y,N]')

    if cont.upper() == 'Y':
        gameover = 0
    elif cont.upper() == 'S':
        print('\n\U0001F916___________________________\U0001F4A3\n|PLAYER PROFILE:[',username,']\n|GAMES PLAYED: ',stt,'\n|GAMES WON:    ',stw,'\n|FASTEST TIME: ',sth,'\n|___________________________\U0001F4A3\n')
        break
    else:
        break

    print('Saving and closing...')

print("\n\U0001F4A3[Textsweeper - Created by: Josh Lo - made in replit] Thanks for playing!\U0001F4A3")