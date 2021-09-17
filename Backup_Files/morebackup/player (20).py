import copy
from itertools import chain
import math

from LUCKY_LALAS.util import print_board, print_slide, print_swing, InputDictConversion, MakeBigDict, updateBigBoardDict


def relocate_tokens(team_dictionary, team_action):

    #print("relocating tokens", team_dictionary)
    # print("relocating tokens, below is the team action inputted")
    #   print(team_action)
     # """ moves tokens for a team, based on the action given. does not take into account tokens being eaten yet??? """

      #action formatted

         #  ("THROW", type, (r, q))
        # (swing/slide, (ra, qa), (rb, qb))

      ## moving tokens, adapted from the "addturn" function in our project 1

      ## if i's a throw
    if team_action[0] == "THROW":
        newcoordinate = team_action[2]
        tokenType = team_action[1]
        #if the cell is already occupied, add it to the list of tokens on the cell
        if newcoordinate in team_dictionary:
            team_dictionary[newcoordinate].append(tokenType)
        #otherwise make an entry indicating a token on that cell
        else:
            team_dictionary[newcoordinate] = [tokenType]
      #if it's a swing or a slide
    else:
        currentcoordinate = team_action[1]
        newcoordinate = team_action[2]
        tokenType= team_dictionary[currentcoordinate][0]
    #     print("tokentype being shifted ", tokenType)
        #slide off token from its current cell's list
        
        team_dictionary[currentcoordinate].pop()
        

        #if entry is empty, remove from dictionary
        if team_dictionary[currentcoordinate] == []:
            del team_dictionary[currentcoordinate]

        #slide token=type onto new cell's list.  corresponds to the new coordinate
        #if entry exsists, append onto it
        if newcoordinate in team_dictionary:
            team_dictionary[newcoordinate].append(tokenType)
        else:
            team_dictionary[newcoordinate] = [tokenType]
    #         print("shifted to an empty spot")
    #         print(team_dictionary[newcoordinate])

   # print("relocated tokens", team_dictionary)
       
        
 
def coordinatesInBoundary(coordinatetuple):
  ##given coordinates, if it's in the boundaries of board
  ## return true, otherwise, return false
  #if row/x is larger than 0
  if coordinatetuple[0] in range(5):
    #y should be more than -4, and be less than 4-x
    if coordinatetuple[1] >= -4 and coordinatetuple[1] <= (4-coordinatetuple[0]):
      return True
  #if row/x is less than 0
  elif coordinatetuple[0] in range(-4,0):
    #y should be less than 4, and be less than -4-x
    if coordinatetuple[1] <= 4 and coordinatetuple[1] >= (-4-coordinatetuple[0]):
      return True
  else:
    return False
  
def rps_fight(firsttokentype, secondtokentype):
      """ given two types, determine who is winner based on who is first.
        returns: 1= 1st token beat 2nd token, 0= tie, -1= 1st token lost to 2nd token 
        
        Taken from our project 1"""
      if firsttokentype == secondtokentype:
        return 0
      elif firsttokentype == "r" and secondtokentype == "p":
        return -1
      elif firsttokentype == "r" and secondtokentype == "s":
        return 1
      elif firsttokentype == "s" and secondtokentype == "r":
        return -1
      elif firsttokentype == "s" and secondtokentype == "p":
        return 1
      elif firsttokentype == "p" and secondtokentype == "s":
        return -1
      elif firsttokentype == "p" and secondtokentype == "r":
        return 1  
    
def getThrows(playerDict, enemyDict, playerTeam, throw_dist, firstturn=False, spec= False):
    #returns a list of all possible throws
    move_lst=[]
    if spec:
        token_type_lst= spec
    else:
        token_type_lst= ["r", "p", "s"]
    # Find throwrange according to team's side of the board
    if playerTeam== "upper":
        throwrange= [throw_dist, 4]
    else:
        throwrange= [-4, throw_dist]
        
    for r in throwrange:
        for q in range(-4, 5):
            if coordinatesInBoundary((r,q)): 
                ## if taken by enemy, only throw if you win
                if enemyDict.get((r,q)):
                    for token_type in token_type_lst:
                        if rps_fight(token_type, enemyDict.get((r,q)))==1:
                            move_lst.append(("THROW" ,token_type, (r,q)))
                ## if taken by team member, only throw if they are the same coordinate
                if playerDict.get((r,q)):
                    for token_type in token_type_lst:
                        if rps_fight(token_type, playerDict.get((r,q)))==0:
                            move_lst.append(("THROW" ,token_type, (r,q)))
                else:
                    for token_type in token_type_lst:
                        if firstturn:
                            return "THROW" ,token_type, (r,q)
                        move_lst.append(("THROW" ,token_type, (r,q)))
    return move_lst
    
def check_instant_kill(enemydict, playerthrowdist, playerteam):
    tokentypes=('r','p','s')
    if playerteam=="upper":
        start_row= 4
        throwrange= (playerthrowdist, start_row+1)
    else:
        start_row= -4
        throwrange= (start_row, playerthrowdist+1)
    print(throwrange)
    for r in range(throwrange[0],throwrange[1]):
        print(r)
        for q in range(-4,4):
            coordinatetuple= (r,q)
            enemytokentype= enemydict.get(coordinatetuple)
            if coordinatesInBoundary(coordinatetuple) and enemytokentype:
                for tokentype in tokentypes:
                    if rps_fight(tokentype, enemytokentype)==1:
                        return "THROW", tokentype, coordinatetuple
    return 0
                    
def getSlides(cell, tokentype, playerDict, enemyDict, is_swing=0, og_coordinate=False): 
    # returns a list of all possible slides
    # og_coordinate is only True when is_swing is True. It is the coordinate where the coordinate is swinging from. In the case,
    # of a swing, the cell argument is the adjacent token to the original token.
    move_lst=[]
    sorted_move_dict= {1: [], 0: []}
    r= cell[0]
    q= cell[1]
    token_type= tokentype### get token_type
    r_lst= [r+1, r+1, r, r, r-1, r-1]
    q_lst= [q-1, q, q-1, q+1, q, q+1]
    if is_swing:
        o_r= og_coordinate[0]
        o_q= og_coordinate[1]
        o_r_lst= [o_r+1, o_r+1, o_r, o_r, o_r-1, o_r-1]
        o_q_lst= [o_q-1, o_q, o_q-1, o_q+1, o_q, o_q+1]
    r_directions=[]
    q_directions=[]
    
    #when it's not a slide as part of getSwings(), the original coordinate is the same as the cell coordinate
    dont_add=0
    if og_coordinate:
        for i in range(len(r_lst)):
            if (r_lst[i],q_lst[i]) == og_coordinate:
                dont_add=1
            for o_r,o_q in zip(o_r_lst, o_q_lst):
                if (r_lst[i],q_lst[i]) ==(o_r, o_q):
                    dont_add=1
            if dont_add==0:
                r_directions.append(r_lst[i])
                q_directions.append(q_lst[i])
            else:
                dont_add=0
    else:
        og_coordinate = cell
        r_directions= r_lst
        q_directions= q_lst
    for i,j in zip(r_directions, q_directions):
        unsorted_move_dict= validMove(sorted_move_dict, playerDict, enemyDict, token_type, og_coordinate,(i,j))
        
    #convert unsorted_move_dict to a sorted move list
    for key in sorted_move_dict:
        for i in sorted_move_dict[key]:
            move_lst.append(i)
            
    for iterator in range(0,len(move_lst)):
        move_lst[iterator] = ["SLIDE"] + move_lst[iterator]
    
    
    return move_lst
  

def getSwings(cell, tokentype, playerDict, enemyDict):
  #addSwings returns a list of possible swing moves
  move_lst= []
  ##gets a list of adjacent tokens of the same team and find the slide moves possible from the adjacent tokens
  adjToklst= findAdjacentTok(playerDict, cell) 
  for adjTok in adjToklst:
    temp_move_lst= getSlides(adjTok, tokentype, playerDict, enemyDict, 1, cell)
    move_lst= move_lst + temp_move_lst
  for iterator in range(0,len(move_lst)):
    #change the SLIDES that are in movelist to SWINGS    
    move_lst[iterator][0] = "SWING"
    
  return move_lst
  
def findAdjacentTok(playerDict, cell):
  #This function returns a list of coordinates for adjacent tokens  
  AdjacentToklst = []
  r= cell[0]
  q= cell[1]
  r_directions= [r+1, r+1, r, r, r-1, r-1]
  q_directions= [q-1, q, q-1, q+1, q, q+1]
  for i,j in zip(r_directions, q_directions):
    if playerDict.get((i, j)):
      AdjacentToklst.append((i,j))
  return AdjacentToklst



def validMove(unsorted_move_dict, playerDict, enemyDict, tok_type, coordinate_a, coordinate_b):
    # This function adds a direction token to the move_lst
    # COMPATIBLE ONLY WITH GETSLIDES AND GETSWINGS
    player_tok= playerDict.get(coordinate_b)
    enemy_tok= enemyDict.get(coordinate_b)
    
    #take the first token type of the list if more than one token on the coordinatesince they are all same type either way
    if type(player_tok)==list:
        player_tok= player_tok[0]
    #ensures the enemy_tok is  of type list
    if enemy_tok!= None:
        if type(enemy_tok)!= list:
            enemy_tok= list(enemy_tok) 
    #when faced with token of the opposing team, ties and winning are the only valid move
        for enemy_tok_type in enemy_tok:
            fight_res= rps_fight(tok_type, enemy_tok_type)
            if fight_res!=-1:
                movenode= [coordinate_a, coordinate_b, tok_type]
                unsorted_move_dict[fight_res].append(movenode)
# if it is within or the boundaries and there is no other token or blocks, add to directions
    if  enemy_tok==None and (player_tok==None or player_tok== tok_type) and coordinatesInBoundary(coordinate_b): ## if uppertok is the same
        movenode= [coordinate_a, coordinate_b, tok_type]
        unsorted_move_dict[0].append(movenode)
    return unsorted_move_dict

def minimax(playerDict, enemyDict, playerTeam, enemyTeam, 
        playerMaxThrow, enemyMaxThrow, 
        self_throws_did, enemy_throws_did,
        depth, maxdepth,  
        initialplayereaten, initialenemyeaten, currentplayereaten, currentenemyeaten,
         current_turn, maximise=True):
    # check if we can return value
    
    
    
    
    #return_val= eval(playerDict, enemyDict, depth, maxdepth, initialplayertokenseaten, initialenemytokenseaten)
    #this section needs to be looked at/fixed.
    return_val= evaluation(playerDict, enemyDict, depth, maxdepth, 
        initialplayereaten, initialenemyeaten, currentplayereaten, currentenemyeaten)
    
    
    if return_val!= "continue_minimax":
        #print("continue")
        return return_val
        
        
        
        
    #else continute minimax process
    if maximise:
        
        bestval= float('-inf')
        for cell, tokenTypes in playerDict.items():
            for tokenType in tokenTypes:
                
            
            
                slidesTemporary = getSlides(cell, tokenType, playerDict, enemyDict)
                swingsTemporary = getSwings(cell, tokenType, playerDict, enemyDict)
                
              #generate throws only when not swings and slides possible
                if playerMaxThrow<9 and ((len(slidesTemporary)==0 and len(swingsTemporary)==0) or find_team_sufficiency_value(playerDict, enemyDict)==0):
                        missingtokentypes= find_missing_teamtokentype(playerDict, enemyDict)
                        throwsTemporary= getThrows(playerDict, enemyDict, playerTeam, playerMaxThrow,spec= missingtokentypes)
                else:
                    throwsTemporary = []
                    
                possibleMovelst= slidesTemporary + swingsTemporary + throwsTemporary
                
                for possibleMove in possibleMovelst:
                    playerdictcopy= copy.deepcopy(playerDict)
      #              print("minimax -inf relocating tokens of playerdict")
      #              print(playerdictcopy)
                    relocate_tokens(playerdictcopy, possibleMove)
       #             print(playerdictcopy)
                   # update_tokens_eaten(playerDict, enemyDict)
       
                    
                    #need to take into account the number of throws done 
                    if possibleMove[0] == "THROW":
                            
                        return minimax(playerdictcopy, enemyDict,
                            playerTeam, enemyTeam, 
                            playerMaxThrow, enemyMaxThrow,
                            self_throws_did+1, enemy_throws_did,
                            depth+1, maxdepth,
                            initialplayereaten, initialenemyeaten,
                            currentplayereaten, currentenemyeaten,
                            current_turn, False)
                            
                    else:
                        return minimax(playerdictcopy, enemyDict,
                            playerTeam, enemyTeam, 
                            playerMaxThrow, enemyMaxThrow,
                            self_throws_did, enemy_throws_did,
                            depth+1, maxdepth,
                            initialplayereaten, initialenemyeaten,
                            currentplayereaten, currentenemyeaten,
                            current_turn, False)
            
    else:
    
    
        #GENERATE ENEMY DICTS/ POSSIBLE BOARD STATES FOR THE ENEMY
        
        generated_enemydicts = []
        
        bestval= float('inf')
        for cell, tokenTypes in enemyDict.items():
            for tokenType in tokenTypes:
                slidesTemporary = getSlides(cell, tokenType, enemyDict, playerDict)
                swingsTemporary = getSwings(cell, tokenType, enemyDict, playerDict)
                
                #don't generate enemy throws if already thrown 9 tokens
                if enemyMaxThrow<9 and ((len(slidesTemporary)==0 and len(swingsTemporary)==0) or find_team_sufficiency_value(enemyDict, playerDict)==0):
                        missingtokentypes= find_missing_teamtokentype(enemyDict, playerDict)
                        throwsTemporary= getThrows(enemyDict, playerDict, enemyTeam, enemyMaxThrow, spec= missingtokentypes)
                else:
                    throwsTemporary = []
                    
                possibleMovelst= slidesTemporary + swingsTemporary + throwsTemporary
                
                for possibleMove in possibleMovelst:
     #               print("minimax inf relocating tokens of enemydict")
                    enemydictcopy= copy.deepcopy(enemyDict)
      #              print(enemydictcopy)
                    relocate_tokens(enemydictcopy, possibleMove)
                   # update_tokens_eaten(playerDict, enemyDict)
      #              print(enemydictcopy)
      
                    #the zero at the end, is the "score" for how good that board is
                    generated_enemydicts.append([enemydictcopy, possibleMove, 0])
      
      
      
      
      
      
      
      
      
                    if possibleMove[0] == "THROW":
                            ####################### NOOOOOTE ENEMYDICT SHOULD BECOME ENEMYDICT COPY IN A LATER STAGE
                            
                        return minimax(playerDict, enemyDict, 
                            playerTeam, enemyTeam,
                            playerMaxThrow, enemyMaxThrow, 
                            self_throws_did, enemy_throws_did+1,
                            depth+1, maxdepth,
                            initialplayereaten, initialenemyeaten, 
                            currentplayereaten, currentenemyeaten, 
                            current_turn)
                            
                    else:
                        return minimax(playerDict, enemyDict, 
                            playerTeam, enemyTeam,
                            playerMaxThrow, enemyMaxThrow, 
                            self_throws_did, enemy_throws_did,
                            depth+1, maxdepth,
                            initialplayereaten, initialenemyeaten, 
                            currentplayereaten, currentenemyeaten, 
                            current_turn)


def evaluation(playerDict, enemyDict, depth, maxdepth, 
    initialplayereaten, initialenemyeaten, currentplayereaten, currentenemyeaten, maximum=True): 
  #  print("evaluation function")
 #   print("depth", depth)
    #player wins and eats
    if initialenemyeaten > currentenemyeaten:
        return 100
    #player loses and gets eaten
    elif initialplayereaten > currentplayereaten:
        return -100
    #reached depth limit
    elif depth==maxdepth:
        #check if enough tokens to win 
       # playerdict_tokens_on_board= sum(len(v) for v in playerDict.values())
       # enemydict_tokens_on_board= sum(len(v) for v in enemyDict.values())
       # tokens_diff= abs(playerdict_tokens_on_board- enemydict_tokens_on_board)
       # tokens_diff_usefulness=(1-tokens_diff/depth)
       # if (tokens_diff_usefulness>1):
       #     exit()
        # check if has right tokens to win
        player_sufficient_tokens= find_team_sufficiency_value(playerDict, enemyDict)
        enemy_sufficient_tokens= find_team_sufficiency_value(enemyDict, playerDict)
        sufficiency_diff= player_sufficient_tokens - enemy_sufficient_tokens
        #heuristic function
        if player_sufficient_tokens!=0:
#            print("player_sufficient_tokens!=0")
            team_board_value= find_team_dist_value(playerDict, enemyDict)
        else:
            team_board_value= 0
        if enemy_sufficient_tokens!=0:
  #          print("enemy_sufficient_tokens")
            opposing_team_board_value= find_team_dist_value(enemyDict, playerDict)
        else:
            opposing_team_board_value= 0
        board_value= team_board_value - opposing_team_board_value
        #print("playerDict", playerDict)
        #print("enemyDict", enemyDict)
  #      if board_value>0:
  #          print("sufficiency_diff",sufficiency_diff)
   #         print("board value:",board_value)
        return board_value*80+ sufficiency_diff*20
    
    return "continue_minimax"



def create_teamtokens_on_board(team):
    ##### make a list of unique token types given a team dictionary
    temp_team_types_list = []
    for list_of_tokens in team.values(): 
        for one_token in list_of_tokens:
            temp_team_types_list.append(one_token)
    team_types= list(set(temp_team_types_list))
    return team_types
              
def find_missing_teamtokentype(team, opposing_team):
    ## returns a list of missing token types given a team dictionary
    team_types= create_teamtokens_on_board(team)
    opposing_team_types= create_teamtokens_on_board(opposing_team)
    # store the missing token type necessary to beat
    is_beaten=0
    missing_teamtokentype= []
    for y in opposing_team_types:
            for x in team_types:
                if rps_fight(x, y)==1:
                    is_beaten=1
                    break
            if is_beaten==0:
                for i in ['r','p','s']:
                    if rps_fight(i,y)==1:
                        missing_teamtokentype.append(i)
            else:
                is_beaten=0
    return missing_teamtokentype
        
def hex_dist_val(p,q):
    curr_sum=0
    ## find the  distance between points p (r,q) and q (r,q)
    #if going left
    if q[1]<p[1]:
        dist1= q[0]-p[0]
        if q[0]>p[0]:
            #simulaneously goes up
            new =p[1]-abs(dist1)
            dist2= new - q[1]
        # goes down
        else:
            dist2= q[1]-p[1]
    # if going right:
    else:
        dist1= q[0] - p[0]
        #if going up
        if q[0]>p[0]:
            dist2= q[1]-p[1]
        # simulaneously going down
        else:
            new= p[1]-dist1
            dist2= q[1] - new
    return abs(dist1)+ abs(dist2)
            
            
    return curr_sum

def find_team_dist_value(team, opposing_team):
    ## find the dista
    #closest_o_coordinate is a list which gives the closest opposing team weak token corresponding to 
    # the coordinates in team.key()
    #print(team)
    #print(opposing_team)
    sum_team_dist=0
    for t_coordinate, t_toktypes in team.items():
 #       print("team dictionary in find_team_dist_value", team)
        closest_dist= 100000
        tokens_closest_dist_not_calc= 0
        curr_closest_o_coordinate= None
        for o_coordinate, o_toktypes in opposing_team.items():
            # convert to string
            #print("t_toktypes", t_toktypes)
            if type(t_toktypes)==list:
                t_toktypes= t_toktypes[0]
            if type(o_toktypes)==list:
                o_toktypes= o_toktypes[0]
            if rps_fight(t_toktypes, o_toktypes)==1:
                curr_dist= hex_dist_val(t_coordinate, o_coordinate)
                curr_dist= hex_dist_val(t_coordinate, o_coordinate)
                #if(curr_dist>9):
                #    print(t_coordinate, o_coordinate)
                #    print(curr_dist)
                #    exit()
                if curr_dist< closest_dist:
                    closest_dist= curr_dist
        if closest_dist==100000:
            tokens_closest_dist_not_calc= tokens_closest_dist_not_calc + 1
        else:
            sum_team_dist= sum_team_dist + closest_dist
    
  #  if len(team.keys())- tokens_closest_dist_not_calc==0:
   #     print(team, opposing_team)
   #     print(len(team.keys()))
   #     print(tokens_closest_dist_not_calc)
   #     exit()
    #Transform data to be comparable in the form log(1-ave_team_dist*10/9)
    if (len(team.keys())- tokens_closest_dist_not_calc) != 0:
    
        ave_team_dist= sum_team_dist/(len(team.keys())- tokens_closest_dist_not_calc)* 10/9
        
    else:
        ave_team_dist = 0
    #print("log", math.log(ave_team_dist,10))
    #print()
    #exit()
    
    if ave_team_dist == 0:
        return 1
    else:
        return 1-math.log(ave_team_dist,10)
   
    
         
                
            
def find_team_sufficiency_value(team, opposing_team):

###makes a value based on how many of team's tokens can beat opposing team's
    team_types=create_teamtokens_on_board(team)
    opposing_team_dict={}
    for coordinate_tokens in opposing_team.values():
        if type(coordinate_tokens)==list:
            for token in coordinate_tokens:
                if token in opposing_team_dict:
                    opposing_team_dict[token]= opposing_team_dict[token]+1
                    #otherwise make an entry indicating a token on that cell
                else:
                    opposing_team_dict[token] = 1
        else:
            if coordinate_tokens in opposing_team_dict:
                opposing_team_dict[coordinate_tokens]= opposing_team_dict[coordinate_tokens]+1
                    #otherwise make an entry indicating a token on that cell
            else:
                opposing_team_dict[coordinate_tokens] = 1
                
                
                
                
    if len(team_types)<3:
        oppteam_weakertypes=[]
        for x in team_types:
            for y in opposing_team_dict.keys():
                #try fighting against the other types to see if you 
                if rps_fight(x, y) == 1:
                    oppteam_weakertypes.append(y)
        oppteam_tottokens= sum(opposing_team_dict.values())
        team_totpower=0
        
        for toktype in oppteam_weakertypes:
            team_totpower= team_totpower+ opposing_team_dict[toktype]
            
        #for avoiding zero division error
        if oppteam_tottokens != 0:      
            team_power= team_totpower/oppteam_tottokens
        else:
            team_power = 1
    else:
        team_power= 1
        
    return team_power
            


def update_tokens_eaten(dict1, dict2):
    # """ given two dictionaries, removes tokens in both dictionaries based on who gets eaten"""

    #amount of tokens dict 1 eats is in first position,
    #amount of tokens dict2 eats is in second position
    temp_eatslist = [0,0]


    #  print()
    #  print("running update tokens eaten on")
    #  print("dict 1", dict1)
    #  print("dict2", dict2)
    #first find if the dictionaries have matching coordinate keys, indicating the prescence of  tokens on that spot

    #comparing cells  
    for dict1_coordinate in dict1:
        for dict2_coordinate in dict2:
        
        
            # if tokens from two different teams are sitting on the same spot 
            if dict1_coordinate == dict2_coordinate:

                dict1_token_list = dict1[dict1_coordinate]
                dict2_token_list = dict2[dict2_coordinate]


                ## remove tokens eating each other from different dictionaries, on the same cell

                #these  lists is so if three tokens of three different types, but different teams, sit on each other
                #they can call be annihilated at the same time.
                ## one square may contain a P, S and a r. They all need to die, but if r removes S, P still needs to be eaten
                ## by S

                recently_removed_from_dict1 = []
                recently_removed_from_dict2 = []

                for token1 in dict1_token_list:
                    for token2 in dict2_token_list:
                        fight_result = rps_fight(token1, token2)

                        #if first token won
                        if fight_result == 1:

                      #      print("token removed from 2nd dict")                                 
                            recently_removed_from_dict2.append(token2)
                            temp_eatslist[0] = temp_eatslist[0] + 1
                     #       print("first token won at", dict1_coordinate)

                        #if second token won
                        elif fight_result == -1:
                        #    print("token removed from 1st dict")  
                            recently_removed_from_dict1.append(token1)
                            temp_eatslist[1] = temp_eatslist[1] + 1
                       #     print("second token won at", dict1_coordinate)
                            
                            
                #tokens removed now, to prevent skipping over tokens when deleting them
                for token in recently_removed_from_dict1:
                    if token in dict1_token_list:
                        dict1_token_list.remove(token)
                    
                for token in recently_removed_from_dict2:
                    if token in dict2_token_list:
                        dict2_token_list.remove(token)    
                
                removed_cannibalism_list1 = []
                removed_cannibalism_list2 = []
                
                ## remove tokens eating each other, but within the same dictionary / self cannibalism
                for token1 in dict1_token_list:
                    for removed_token_1 in recently_removed_from_dict1:


                        fight_result = rps_fight(removed_token_1, token1)

                        #if a recently removed token wins, remove token one
                        #give a victory to the other team

                        if fight_result == 1:
                            removed_cannibalism_list1.append(token1)
                            temp_eatslist[1] = temp_eatslist[1] + 1
                        #    print("removed a coordinate cannibal 1")



                for token2 in dict2_token_list:
                    for removed_token_2 in recently_removed_from_dict2:


                        fight_result = rps_fight(removed_token_2, token2)

                        #if a recently removed token wins, remove token two
                        #give victory to other team

                        if fight_result == 1:
                            removed_cannibalism_list2.append(token2)   
                            temp_eatslist[0] = temp_eatslist[0] + 1
                    #        print("removed a coordinate cannibal 2")                            

                #removing cannibalised tokens
                for token in removed_cannibalism_list1:
                    if token in dict1_token_list:
                        dict1_token_list.remove(token)
                    
                for token in removed_cannibalism_list2:
                    if token in dict2_token_list:
                        dict2_token_list.remove(token)                

    #self cannibalism check, but for when it's not between two teams  
    
    
    
                
    #for cannibalism, give victories to other team.  
    
    # for every cell stored
    for dict1_coordinate in dict1:
        
        
        dict1_token_list = dict1[dict1_coordinate]
        
        #keeps track of who gets cannibalised
        removed_cannibalism_list1 = []
        
        fight_result = 0
        
        #make it fight agaist itself
        for a_token in dict1_token_list:
        
            
            
            for b_token in dict1_token_list:
            
                #print("THESE TOKENS ARE FIGHTING", a_token, b_token)
            
                
            
                fight_result = rps_fight(a_token, b_token)
                
                if fight_result == 1:
                    removed_cannibalism_list1.append(b_token)
                    temp_eatslist[1] = temp_eatslist[1] + 1
                #    print("first token won in lone self cannibalsim")
                    
                
                #if second token won
                elif fight_result == -1:
                    removed_cannibalism_list1.append(a_token)
                    temp_eatslist[1] = temp_eatslist[1] + 1
              #      print("second token won in lone self cannibalsim")
                    
                    
                    
                #if one token has won
                if fight_result != 0:
               #     print("a token won in lone self cannibalism")
               #     print("cannibalism list and token dict")
               #     print("removed_cannibalism_list1",removed_cannibalism_list1)
               #     print("dict1tokenlist", dict1_token_list)
                    #remove all tokens of the type that lost
                    for tokentype in removed_cannibalism_list1:
                        for token in dict1_token_list:
                            if tokentype == token:
                                dict1_token_list.remove(token)  
                #                print("lone self cannibalism removed")
                #                print("dict1tokenlist", dict1_token_list)
                    
                    #breaks token b loop
                    break
                    
            #breaks token a loop, so we will now look at another cell
            if fight_result != 0:
                break
     
    #doing self cannibalism for dict 2
    
    # for every cell stored
    for dict2_coordinate in dict2:
        
        
        dict2_token_list = dict2[dict2_coordinate]
        
        #keeps track of who gets cannibalised
        removed_cannibalism_list2 = []
        
        fight_result = 0
        
        #make it fight agaist itself
        for a_token in dict2_token_list:
        
            
            
            for b_token in dict2_token_list:
            
                #print("THESE TOKENS ARE FIGHTING", a_token, b_token)
            
                
            
                fight_result = rps_fight(a_token, b_token)
                
                if fight_result == 1:
                    removed_cannibalism_list2.append(b_token)
                    temp_eatslist[0] = temp_eatslist[0] + 1
    #                print("first token won in lone self cannibalsim")
                    
                
                #if second token won
                elif fight_result == -1:
                    removed_cannibalism_list2.append(a_token)
                    temp_eatslist[0] = temp_eatslist[0] + 1
    #                print("second token won in lone self cannibalsim")
                    
                    
                    
                #if one token has won
                if fight_result != 0:
     #               print("a token won in lone self cannibalism")
     #               print("cannibalism list and token dict")
     #               print("removed_cannibalism_list2",removed_cannibalism_list2)
     #               print("dict2tokenlist", dict2_token_list)
                    #remove all tokens of the type that lost
                    for tokentype in removed_cannibalism_list2:
                        for token in dict2_token_list:
                            if tokentype == token:
                                dict2_token_list.remove(token)  
     #                           print("lone self cannibalism removed")
     #                           print("dict2tokenlist", dict2_token_list)
                    break
                    
            
            if fight_result != 0:
                break
     
     
   
   
    # removing a coordinate's empty lists the cell's tokens are all eaten
  
    removelistdict1 = []
    for coordinate in dict1:
        if dict1[coordinate] == []:
            removelistdict1.append(coordinate)
                
                #this the removelists is so u don't run into iteration error
    for coordinate in removelistdict1:
        del dict1[coordinate]
    
    
    
    removelistdict2 = []
    for coordinate in dict2:
        if dict2[coordinate] == []:
            removelistdict2.append(coordinate)
            
    for coordinate in removelistdict2:
        del dict2[coordinate]            
                
 #   print("ran update tokens eaten on")
 #   print("dict 1", dict1)
  #  print("dict2", dict2)
  #  print("temp_eatslist", temp_eatslist)
  #  print()
    return temp_eatslist



#########
#function clones kinda
#they're the same, but modified.

#minimax clone

def move_against(playerDict, enemyDict, playerTeam, player_throws_did, player_throw_distance):
    
    
    #for the player team,
    for cell, tokenTypes in playerDict.items():
            
            tokenType= tokenTypes[0]
            #generate slides and swings
            
            slidesTemporary = getSlides(cell, tokenType, playerDict, enemyDict)
            swingsTemporary = getSwings(cell, tokenType, playerDict, enemyDict)
            
          #generate throws only when not swings and slides possible
            if player_throws_did<9 and find_team_sufficiency_value(playerDict, enemyDict)==0 :
        
            #if player_throws_did < 9:
          
                                    
                missingtokentypes= find_missing_teamtokentype(playerDict, enemyDict)
                
                throwsTemporary= getThrows(playerDict, enemyDict, playerTeam, player_throw_distance ,spec= missingtokentypes)
                    
            else:
                throwsTemporary = []
            
            #  now you have a list of all possible moves for that player, 
            # generate the dictionaries that result from these moves
            
            possibleMovelst= slidesTemporary + swingsTemporary + throwsTemporary
                #playerDictcopy= copy.deepcopy(playerDict)
  #              print("minimax -inf relocating tokens of playerdict")
  #              print(playerdictcopy)
                #relocate_tokens(playerDictcopy, possibleMove)
                
                # zero is because the board hasn't been scored yet.
                #listofpossibledicts.append([playerDictcopy, possibleMove, 0])
                
                
    #now that you have generated the possible boards, it is time to score them.
    
    #currently_best_score = float('-inf') 
   # bestPossibleBoard_and_move = []
    #for potential_state in listofpossibledicts:
        
        #give the board a score
        #[generated_dict, move that caused the generated dict, board score of how good it is]
        
        #potential_board = potential_state[0]
        #score = evaluate(potential_board,enemyDict)
        
       # potential_state[2] = score
        
        #if the score is really good, replace it as the best possible board/move
       # if score >= currently_best_score:
            #currently_best_score = score
            #bestPossibleBoard_and_move = potential_state
    
  #  print("list of possible dicts", listofpossibledicts)
         #[dict, move, score] 
         
    return possibleMovelst




def evaluate(playerDict, enemyDict): 
    
  #  print("evaluation function")
 #   print("depth", depth)
    #player wins and eats
    
    score = 0
    
    scoringPlayerDict = copy.deepcopy(playerDict)
    scoringEnemyDict = copy.deepcopy(enemyDict)
    
    temp_eatslist = update_tokens_eaten(scoringPlayerDict, scoringEnemyDict)
    playereats = temp_eatslist[0]
    enemyeats = temp_eatslist[1]
    ## if this move causes an enemy token to be eaten
    if playereats > enemyeats:
        score = score + 100
    #player loses and gets eaten
    elif enemyeats > playereats:
        score = score - 100
       
    
    #check if enough tokens to win 
   # playerdict_tokens_on_board= sum(len(v) for v in playerDict.values())
   # enemydict_tokens_on_board= sum(len(v) for v in enemyDict.values())
   # tokens_diff= abs(playerdict_tokens_on_board- enemydict_tokens_on_board)
   # tokens_diff_usefulness=(1-tokens_diff/depth)
   # if (tokens_diff_usefulness>1):
   #     exit()
   
   
    # check if has right tokens to win
    player_sufficient_tokens= find_team_sufficiency_value(playerDict, enemyDict)
    enemy_sufficient_tokens= find_team_sufficiency_value(enemyDict, playerDict)
    sufficiency_diff= player_sufficient_tokens - enemy_sufficient_tokens
    
    #heuristic function based on distance
    if player_sufficient_tokens!=0:
#            print("player_sufficient_tokens!=0")
        team_board_value= find_team_dist_value(playerDict, enemyDict)
    else:
        team_board_value= 0
        
        
    if enemy_sufficient_tokens!=0:
#          print("enemy_sufficient_tokens")
        opposing_team_board_value= find_team_dist_value(enemyDict, playerDict)
    else:
        opposing_team_board_value= 0
        
        
    board_value= team_board_value - opposing_team_board_value
    
    
    #print("playerDict", playerDict)
    #print("enemyDict", enemyDict)
#      if board_value>0:
#          print("sufficiency_diff",sufficiency_diff)
#         print("board value:",board_value)


    score = score + board_value*95+ sufficiency_diff*5
    return score
    
    
    
    
######### end of cloned functions #########



#######################
##########################
############# CLASS PLAYERRRRRRRRRRRRRRRRRRRRRRRR #########################################
#######################
####################
########################


        
class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here
        
        
        self.team = player
        
        if  player == "upper":
            self.enemyteam = "lower"
            # keeping track of how far the payer can throw a token
            self.self_throw_distance = 4
        
            # keeping track of how far the enemy can throw their token
            self.enemy_throw_distance = -4
        else:
            self.enemyteam = "upper"
            # keeping track of how far the payer can throw a token
            self.self_throw_distance = -4
        
            # keeping track of how far the enemy can throw their token
            self.enemy_throw_distance = 4
        
        self.self_throws_did = 0
        
        self.enemy_throws_did = 0
        
        #current location of all your own tokens
        self.selfdict = {}
 
        #how many of your own tokens have been eaten
        self.self_losses = 0
        
        
        #current location of enemy tokens
        self.enemydict = {}
        
        #how many enemy tokens we have eaten
        self.enemy_losses = 0
        
        
        #beginning at turn 1.
        self.current_turn = 1
        
        
        
          
    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
       # print("at the beginning of action function")
       # print("selfict")
       # print(self.selfdict)
       # print("enemydict")
       # print(self.enemydict)
        if check_instant_kill(self.enemydict, self.self_throw_distance, self.team):
            return check_instant_kill(self.enemydict, self.self_throw_distance, self.team)
            
        #if the game has just started/ current dictionary is empty, just randomly throw a piece on the board
        if (len(self.selfdict)==0 or find_team_sufficiency_value(self.selfdict, self.enemydict)<1) and self.self_throws_did<9:
            missingtokentypes= find_missing_teamtokentype(self.selfdict, self.enemydict)
            return getThrows(self.selfdict, self.enemydict, self.team, self.self_throw_distance, firstturn= True, spec= missingtokentypes)
        #if no enemy piece on board, just randomly slide a token
        elif len(self.enemydict)==0 and self.self_throws_did<9:
            action= getSlides(cell, tokenType, self.selfdict, self.enemydict)[0]
            return tuple(action[0:3])
       # if self.current_turn>2:
       #     exit()
        
        
        ##otherwise, think of a cleverer action
        
        action= None
        
        
        #first predict what the enemy might do, based on what it can see from our current board?
        
        #def move_against(playerDict, enemyDict, playerTeam, player_throws_did, player_throw_distance):
    
        #[dict, move, score] enemy prediction is this kind of list 
   #     print()
   #     print("enemy predicting...")
        selfprediction = move_against(self.selfdict, self.enemydict, self.team, self.self_throws_did, self.self_throw_distance)
        enemyprediction = move_against(self.enemydict, self.selfdict, self.enemyteam, self.enemy_throws_did, self.enemy_throw_distance)
        
       
        #then based on what we predicted the enemy could do, we make our move?
  #      print("enemy prediction is...")
  #      print(enemyprediction)
        #if enemyprediction == []:
          #  enemypredicted_dict = {}
       # else:
           # enemypredicted_dict = enemyprediction[0]
        
  #      print()
  #      print("player predicting...")
    #    print("self dict?", self.selfdict)
        currently_best_score = float('-inf')
        for selfpossibleaction in  selfprediction:
            for enemypossibleaction in enemyprediction:
                playerDictcopy= copy.deepcopy(self.selfdict)
                enemyDictcopy= copy.deepcopy(self.enemydict)
                #print(playerDictcopy,selfpossibleaction)
                #exit()
                relocate_tokens(playerDictcopy, selfpossibleaction)
                relocate_tokens(enemyDictcopy, enemypossibleaction)
                #temp_eatslist = update_tokens_eaten(playerDictcopy, enemyDictcopy) 
                score = evaluate(playerDictcopy,enemyDictcopy)
                if score >= currently_best_score:
                    currently_best_score = score
                    action = selfpossibleaction
                
        
        #below statement is for debugging purposes
        #it is better at finding errors
       # player_choice = move_against(self.selfdict, self.enemydict, self.team, self.self_throws_did, self.self_throw_distance)
    
  #      print("player choice", player_choice)
  #      print()
        

       #bestEval= float('-inf') 
       # print(self.selfdict)
       # print(self.enemydict)
        #Traverse all team pieces on board, evaluate minimax eval for each possible move
    #    for cell, tokenTypes in self.selfdict.items():
     #       for tokenType in tokenTypes:
      #          slidesTemporary = getSlides(cell, tokenType, self.selfdict, self.enemydict)
       #         swingsTemporary = getSwings(cell, tokenType, self.selfdict, self.enemydict)
                #generate throws only when not swings and slides possible
        #        if self.self_throw_distance<9 and ((len(slidesTemporary)==0 and len(swingsTemporary)==0) or find_team_sufficiency_value(self.selfdict, self.enemydict)==0):
         #               missingtokentypes= find_missing_teamtokentype(self.selfdict, self.enemydict)
          #              throwsTemporary= getThrows(self.selfdict, self.enemydict, self.team, self.self_throw_distance, spec= missingtokentypes)
           #     else:
            #        throwsTemporary = []
                    
             #   possibleMovelst= slidesTemporary + swingsTemporary+ throwsTemporary
                
  #              print("below is possible moves list")
   #             print(possibleMovelst)
              #  for possibleMove in possibleMovelst:
                
               #     selfdictcopy= copy.deepcopy(self.selfdict)
   #                 print("relocating tokens in actionself, selfdictcopy, pre minimax")
  #                  print(selfdictcopy)
                #    relocate_tokens(selfdictcopy, possibleMove)
                    #update_tokens_eaten(selfdictcopy, self.enemydict)
  #                  print(selfdictcopy)
  
           #         def minimax(playerDict, enemyDict, playerTeam, enemyTeam, 
           #             playerMaxThrow, enemyMaxThrow, 
          #              self_throws_did, enemy_throws_did,
           #             depth, maxdepth,  
           #             initialplayereaten, initialenemyeaten, currentplayereaten, currentenemyeaten,
            #             current_turn, maximise=True):
            
  #                  if possibleMove[0] == "THROW":
   #                     moveEval= minimax(selfdictcopy, self.enemydict, 
    #                        self.team, self.enemyteam, 
     #                       self.self_throw_distance, self.enemy_throw_distance, 
      #                      self.self_throws_did+1, self.enemy_throws_did,
       #                     0, 1, 
        #                    self.self_losses, self.enemy_losses, 
         #                   self.self_losses, self.enemy_losses, 
          #                  self.current_turn, False)
           #         else:
            #            moveEval= minimax(selfdictcopy, self.enemydict, 
             #               self.team, self.enemyteam, 
              #              self.self_throw_distance, self.enemy_throw_distance, 
               #             self.self_throws_did, self.enemy_throws_did,
                #            0, 1, 
                 #           self.self_losses, self.enemy_losses, 
                  #          self.self_losses, self.enemy_losses, 
                   #         self.current_turn, False)
                    
                   # print("move evaluation of", possibleMove, moveEval)
               #     if (moveEval >= bestEval):
                #        action = possibleMove
                 #       bestEval= moveEval
                   #     print("BEST VAL:", bestEval, action)
                  





                  
        #action, if it's a swing/slide, would have a token-type attached to the end
        #but that's invalid format, so it must be chopped off
        if action[0] == "SWING" or action[0] == "SLIDE":
            action = tuple(action[0:3])
            
        return action
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        #action formatted
        # (swing/slide, (ra, qa), (rb, qb))
        # or ("THROW", type, (r, q))
        # put your code here
        
        # add to current turn
       # print("BEFORE UPDATE: self:", self.selfdict, "opposing:", self.enemydict)
        self.current_turn = self.current_turn + 1
  #      print()
  #      print("current turn", self.current_turn)
        #update throw distance
  #      print()
   #     print("calling update function")
   #     print()
  #      print("self dict prerelocation", self.selfdict)
   #     print()
   #     print("enemy dict, prerelocation", self.enemydict)

        #print("player action", player_action)
         # you can increase throw distance no matter where you throw a token onto the board.
        if self.team== "upper":
            
            if opponent_action[0] == "THROW":
                    
                    self.enemy_throw_distance = self.enemy_throw_distance - 1
                    self.enemy_throws_did = self.enemy_throws_did + 1

            if player_action[0] == "THROW":
                    
                    self.self_throw_distance = self.self_throw_distance + 1
                    self.self_throws_did = self.self_throws_did + 1
                    
                    
        else:
        
            
            if opponent_action[0] == "THROW":
                
                    self.enemy_throw_distance = self.enemy_throw_distance + 1
                    self.enemy_throws_did = self.enemy_throws_did + 1

            if player_action[0] == "THROW":
                    
                    self.self_throw_distance = self.self_throw_distance - 1
                    self.self_throws_did = self.self_throws_did + 1
              
   #     print()
        ###  move the tokens for both teams
   #     print("self move", player_action)
   #     print()
   #     print("enemy move", opponent_action)
   #     print()
        
  #      print("Relocating tokens for both teams")
    #    print("now relocating self")
        relocate_tokens(self.selfdict, player_action)
    #    print("self dict post relocation", self.selfdict)
    #    print()
        
   #     print("now relocating enemy")
        relocate_tokens(self.enemydict, opponent_action) 
   #     print("enemy dict, post relocation", self.enemydict)
   #     print()
        
        
    #    debuggerdict = updateBigBoardDict(self.selfdict, self.enemydict, {})
    #    print_board(debuggerdict, "after relocation own dicts", False)
        
        ### see who has been eaten
       
        temp_eatslist = update_tokens_eaten(self.selfdict, self.enemydict)  ### function can be modified
 #       print("Temp eaten list")
       # print("selfdict post being eaten", self.selfdict)
        
  #      print(temp_eatslist)
  #      print()
        # temp eaten list is a list with two values
        # e.g. [5, 7]
        # five would indicate the first dict ate 5 tokens from the other team, the 7 indicates the second 
        # dict eat 7 tokes from the other team.
        self.enemy_losses = self.enemy_losses + temp_eatslist[0]
        self.self_losses = self.self_losses + temp_eatslist[1]
   #     print("AFTER EATEN")
  #      print(" self:", self.selfdict)
   #     print()
   #     print("opposing:", self.enemydict)
   #     print()
        
    #    debuggerdict = updateBigBoardDict(self.selfdict, self.enemydict, {})
    #    print_board(debuggerdict, "after eaten own dicts", False)
        
        
        #print("how many throws did", self.self_throws_did)
     
    

          
    
        


                        


   
  
      

