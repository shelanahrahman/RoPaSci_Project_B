import copy
from itertools import chain
import math
def relocate_tokens(team_dictionary, team_action):
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
        return team_dictionary
    
def update_tokens_eaten(dict1, dict2):
      
     # """ given two dictionaries, removes tokens in both dictionaries based on who gets eaten"""
       
    #    print("update tokens eaten function is running")
      
      #first find if the dictionaries have matching coordinate keys, indicating the prescence of  tokens on that spot
      
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

                    recently_removed_dict1 = []
                    recently_removed_dict2 = []

                    for token1 in dict1_token_list:
                        for token2 in dict2_token_list:
                            fight_result = rps_fight(token1, token2)

                            #if first token won

                            if fight_result == 1:
                                dict2_token_list.remove(token2)
                                recently_removed_dict2.append(token2)

                            #if second token won
                            elif fight_result == -1:
                                dict1_token_list.remove(token1)
                                recently_removed_dict1.append(token1)

                    ## remove tokens eating each other, but within the same dictionary / self cannibalism
                    for token1 in dict1_token_list:
                        for removed_token_1 in recently_removed_dict1:


                            fight_result = rps_fight(removed_token_1, token1)

                            #if a recently removed token wins, remove token one

                            if fight_result == 1:
                                dict1_token_list.remove(token1)



                    for token2 in dict2_token_list:
                        for removed_token_2 in recently_removed_dict2:


                            fight_result = rps_fight(removed_token_2, token2)

                            #if a recently removed token wins, remove token two

                            if fight_result == 1:
                                dict2_token_list.remove(token2)      

          #self cannibalism check, but for when it's not between two teams  

        for dict1_coordinate in dict1:
            dict1_token_list = dict1[dict1_coordinate]

            for a_token in dict1_token_list:
                for b_token in dict1_token_list:
                    fight_result = rps_fight(a_token, b_token)
                    if fight_result == 1:
                        dict1_token_list.remove(a_token)
                    #if second token won
                    elif fight_result == -1:
                        dict1_token_list.remove(b_token)

        for dict2_coordinate in dict2:
            dict2_token_list = dict2[dict2_coordinate]

            for a_token in dict2_token_list:
                for b_token in dict2_token_list:
                    fight_result = rps_fight(a_token, b_token)
                    if fight_result == 1:
                        dict2_token_list.remove(a_token)
                    #if second token won
                    elif fight_result == -1:
                        dict2_token_list.remove(b_token)      

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
            if coordinatesInBoundary((r,q)): ### IF SPACE TAKEN, DONT THROW
                for token_type in token_type_lst:
                    #if enemyDict.get((r,q)) and rps_fight(token_type, enemyDict.get((r,q))):
                    if firstturn:
                        return "THROW" ,token_type, (r,q)
                    move_lst.append(("THROW" ,token_type, (r,q)))
    return move_lst
    
    
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
    r_directions= copy.deepcopy(r_lst)
    q_directions= copy.deepcopy(q_lst)
    
    #when it's not a slide as part of getSwings(), the original coordinate is the same as the cell coordinate
    if og_coordinate:
        for i in range(len(r_lst)):
            if (r_lst[i],q_lst[i]) == og_coordinate:
                r_directions.remove(r_lst[i])
                q_directions.remove(q_lst[i])
                break
    else:
        og_coordinate = cell
        
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
      #              print(enemydictcopy)
      
                    if possibleMove[0] == "THROW":
                            
                            
                        return minimax(playerDict, enemydictcopy, 
                            playerTeam, enemyTeam,
                            playerMaxThrow, enemyMaxThrow, 
                            self_throws_did, enemy_throws_did+1,
                            depth+1, maxdepth,
                            initialplayereaten, initialenemyeaten, 
                            currentplayereaten, currentenemyeaten, 
                            current_turn)
                            
                    else:
                        return minimax(playerDict, enemydictcopy, 
                            playerTeam, enemyTeam,
                            playerMaxThrow, enemyMaxThrow, 
                            self_throws_did, enemy_throws_did,
                            depth+1, maxdepth,
                            initialplayereaten, initialenemyeaten, 
                            currentplayereaten, currentenemyeaten, 
                            current_turn)


def evaluation(playerDict, enemyDict, depth, maxdepth, 
    initialplayereaten, initialenemyeaten, currentplayereaten, currentenemyeaten, maximum=True): 
    
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
            team_board_value= find_team_dist_value(playerDict, enemyDict)
        else:
            team_board_value= 0
        if enemy_sufficient_tokens!=0:
            opposing_team_board_value= find_team_dist_value(enemyDict, playerDict)
        else:
            opposing_team_board_value= 0
        board_value= team_board_value - opposing_team_board_value
        #print("playerDict", playerDict)
        #print("enemyDict", enemyDict)
        print("sufficiency_diff",sufficiency_diff)
        print("board value:",board_value)
        return sufficiency_diff*30+ board_value*70
    
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
        
def euc_dist_val(p,q):
    curr_sum=0
    ## find the euclidean distance between points p and q
    for i in range(len(p)):
        val= pow(p[i]-q[i],2)
        curr_sum= curr_sum+ val
    return pow(curr_sum, 0.5)

def find_team_dist_value(team, opposing_team):
    ## find the dista
    #closest_o_coordinate is a list which gives the closest opposing team weak token corresponding to 
    # the coordinates in team.key()
    #print(team)
    #print(opposing_team)
    sum_team_dist=0
    for t_coordinate, t_toktypes in team.items():
        closest_dist= 100000
        tokens_closest_dist_not_calc= 0
        curr_closest_o_coordinate= None
        for o_coordinate, o_toktypes in opposing_team.items():
            # convert to string
            if type(t_toktypes)==list:
                t_toktypes= t_toktypes[0]
            if type(o_toktypes)==list:
                o_toktypes= o_toktypes[0]
            if rps_fight(t_toktypes, o_toktypes)==1:
                curr_dist= euc_dist_val(t_coordinate, o_coordinate)
                if curr_dist< closest_dist:
                    closest_dist= curr_dist
        if closest_dist==100000:
            tokens_closest_dist_not_calc= tokens_closest_dist_not_calc + 1
        else:
            sum_team_dist= sum_team_dist + closest_dist
    #Transform data to be comparable in the form log(ave_team_dist*10/9)
    print(team)
    print(opposing_team)
    print(sum_team_dist/(len(team.keys())- tokens_closest_dist_not_calc))
    ave_team_dist= sum_team_dist/(len(team.keys())- tokens_closest_dist_not_calc)* 10/9
    #print("log", math.log(ave_team_dist,10))
    #print()
    #exit()
    return math.log(ave_team_dist,10)
    
         
                
            
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
        team_power= team_totpower/oppteam_tottokens
    else:
        team_power= 1      
    return team_power
            


def update_tokens_eaten(dict1, dict2):
     # """ given two dictionaries, removes tokens in both dictionaries based on who gets eaten"""
      
 
      
      #first find if the dictionaries have matching coordinate keys, indicating the prescence of  tokens on that spot
        temp_eatenlist = [0,0]
      
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

                    recently_removed_dict1 = []
                    recently_removed_dict2 = []

                    for token1 in dict1_token_list:
                        for token2 in dict2_token_list:
                            fight_result = rps_fight(token1, token2)

                            #if first token won

                            if fight_result == 1:
                                dict2_token_list.remove(token2)
                                recently_removed_dict2.append(token2)
                                temp_eatenlist[0] = temp_eatenlist[0] + 1

                            #if second token won
                            elif fight_result == -1:
                                dict1_token_list.remove(token1)
                                recently_removed_dict1.append(token1)
                                temp_eatenlist[1] = temp_eatenlist[1] + 1

                    ## remove tokens eating each other, but within the same dictionary / self cannibalism
                    for token1 in dict1_token_list:
                        for removed_token_1 in recently_removed_dict1:


                            fight_result = rps_fight(removed_token_1, token1)

                            #if a recently removed token wins, remove token one

                            if fight_result == 1:
                                dict1_token_list.remove(token1)
                                temp_eatenlist[0] = temp_eatenlist[0] + 1



                    for token2 in dict2_token_list:
                        for removed_token_2 in recently_removed_dict2:


                            fight_result = rps_fight(removed_token_2, token2)

                            #if a recently removed token wins, remove token two

                            if fight_result == 1:
                                dict2_token_list.remove(token2)   
                                temp_eatenlist[1] = temp_eatenlist[1] + 1                                

        #self cannibalism check, but for when it's not between two teams  

        for dict1_coordinate in dict1:
            dict1_token_list = dict1[dict1_coordinate]

            for a_token in dict1_token_list:
                for b_token in dict1_token_list:
                    fight_result = rps_fight(a_token, b_token)
                    if fight_result == 1:
                        dict1_token_list.remove(a_token)
                        temp_eatenlist[0] = temp_eatenlist[0] + 1
                    
                    #if second token won
                    elif fight_result == -1:
                        dict1_token_list.remove(b_token)
                        temp_eatenlist[0] = temp_eatenlist[0] + 1
                        
        for dict2_coordinate in dict2:
            dict2_token_list = dict2[dict2_coordinate]

            for a_token in dict2_token_list:
                for b_token in dict2_token_list:
                    fight_result = rps_fight(a_token, b_token)
                    if fight_result == 1:
                        dict2_token_list.remove(a_token)
                        temp_eatenlist[1] = temp_eatenlist[1] + 1 
                    #if second token won
                    elif fight_result == -1:
                        dict2_token_list.remove(b_token) 
                        temp_eatenlist[1] = temp_eatenlist[1] + 1 
        
        
        #print(temp_eatenlist)
 
        return temp_eatenlist






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
        
        #if the game has just started, just randomly throw a piece on the board
        if self.current_turn==1:
            return getThrows(self.selfdict, self.enemydict, self.team, self.self_throw_distance, True)
        if self.current_turn>2:
            exit()
        
        
        action= None
        bestEval= float('-inf')
        
       # print(self.selfdict)
       # print(self.enemydict)
        #Traverse all team pieces on board, evaluate minimax eval for each possible move
        for cell, tokenTypes in self.selfdict.items():
            for tokenType in tokenTypes:
                slidesTemporary = getSlides(cell, tokenType, self.selfdict, self.enemydict)
                swingsTemporary = getSwings(cell, tokenType, self.selfdict, self.enemydict)
                #generate throws only when not swings and slides possible
                if self.self_throw_distance<9 and ((len(slidesTemporary)==0 and len(swingsTemporary)==0) or find_team_sufficiency_value(self.selfdict, self.enemydict)==0):
                        missingtokentypes= find_missing_teamtokentype(self.selfdict, self.enemydict)
                        throwsTemporary= getThrows(self.selfdict, self.enemydict, self.team, self.self_throw_distance, spec= missingtokentypes)
                else:
                    throwsTemporary = []
                    
                possibleMovelst= slidesTemporary + swingsTemporary+ throwsTemporary
                
  #              print("below is possible moves list")
   #             print(possibleMovelst)
                for possibleMove in possibleMovelst:
                
                    selfdictcopy= copy.deepcopy(self.selfdict)
   #                 print("relocating tokens in actionself, selfdictcopy, pre minimax")
  #                  print(selfdictcopy)
                    relocate_tokens(selfdictcopy, possibleMove)
  #                  print(selfdictcopy)
  
           #         def minimax(playerDict, enemyDict, playerTeam, enemyTeam, 
           #             playerMaxThrow, enemyMaxThrow, 
          #              self_throws_did, enemy_throws_did,
           #             depth, maxdepth,  
           #             initialplayereaten, initialenemyeaten, currentplayereaten, currentenemyeaten,
            #             current_turn, maximise=True):
            
                    if possibleMove[0] == "THROW":
                        moveEval= minimax(selfdictcopy, self.enemydict, 
                            self.team, self.enemyteam, 
                            self.self_throw_distance, self.enemy_throw_distance, 
                            self.self_throws_did+1, self.enemy_throws_did,
                            0, 2, 
                            self.self_losses, self.enemy_losses, 
                            self.self_losses, self.enemy_losses, 
                            self.current_turn, False)
                    else:
                        moveEval= minimax(selfdictcopy, self.enemydict, 
                            self.team, self.enemyteam, 
                            self.self_throw_distance, self.enemy_throw_distance, 
                            self.self_throws_did, self.enemy_throws_did,
                            0, 2, 
                            self.self_losses, self.enemy_losses, 
                            self.self_losses, self.enemy_losses, 
                            self.current_turn, False)
                    
                   # print("move evaluation of", possibleMove, moveEval)
                    if (moveEval >= bestEval):
                        action = possibleMove
                        bestEval= moveEval
                        print("BEST VAL:", bestEval, action)
                        
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
        
        #update throw distance


        
         # you can increase throw distance no matter where you throw a token onto the board.
        if self.team== "upper":
            if opponent_action[0] == "THROW":
                if self.enemy_throws_did!=9:
                    self.enemy_throw_distance = self.enemy_throw_distance - 1
                    self.enemy_throws_did = self.enemy_throws_did + 1

            if player_action[0] == "THROW":
                if self.self_throws_did!=9:
                    self.self_throw_distance = self.self_throw_distance + 1
                    self.self_throws_did = self.self_throws_did + 1
        else:
            if opponent_action[0] == "THROW": 
                if self.enemy_throws_did!=9:
                    self.enemy_throw_distance = self.enemy_throw_distance + 1
                    self.enemy_throws_did = self.enemy_throws_did + 1

            if player_action[0] == "THROW":
                if self.self_throws_did!=9:
                    self.self_throw_distance = self.self_throw_distance - 1
                    self.self_throws_did + self.self_throws_did + 1
              
        
        ###  move the tokens for both teams
        
  #      print("Relocating tokens for both teams")
        self.enemydict= relocate_tokens(self.enemydict, opponent_action)
        self.selfdict= relocate_tokens(self.selfdict, player_action)
        
        ### see who has been eaten
 #       print("Temp eaten list")
        temp_eatenlist = update_tokens_eaten(self.enemydict, self.selfdict)  ### function can be modified
        print(temp_eatenlist)
        # temp eaten list is a list with two values
        # e.g. [5, 7]
        # five would indicate the first dict got 5 tokens eaten/lost, the 7 indicates the second 
        # dict inputted had 7 tokens eaten/lost.
        self.enemy_losses = self.enemy_losses + temp_eatenlist[0]
        self.self_losses = self.self_losses + temp_eatenlist[1]
        #print("AFTER UPDATE: self:", self.selfdict, "opposing:", self.enemydict)
     
    

          
    
        


                        


   
  
      

