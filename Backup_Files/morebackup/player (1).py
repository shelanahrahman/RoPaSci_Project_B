import copy


def relocate_tokens(team_dictionary, team_action):
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

        

            #get token type before moving the token 
            tokenType = team_dictionary[currentcoordinate][0]

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
                
                
def update_tokens_eaten(dict1, dict2):
     # """ given two dictionaries, removes tokens in both dictionaries based on who gets eaten"""
    
      
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
    
def getThrows(playerDict, enemyDict, playerTeam, max_throw_dist, firstturn=False):
    #returns a list of all possible throws
    move_lst=[]
    token_type_lst= ["r", "p", "s"]
    # Find throwrange according to team's side of the board
    if playerTeam== "upper":
        throwrange= [4-max_throw_dist, 4]
    else:
        throwrange= [-4, -4+max_throw_dist]
        
    for r in throwrange:
        for q in range(-4, 5):
            if coordinatesInBoundary((r,q)):
                for token_type in token_type_lst:
                    #if enemyDict.get((r,q)) and rps_fight(token_type, enemyDict.get((r,q))) COULD CONSIDER DIRECT KILL HERE
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
    return move_lst
  

def getSwings(cell, tokentype, playerDict, enemyDict):
  #addSwings returns a list of possible swing moves
  move_lst= []
  ##gets a list of adjacent tokens of the same team and find the slide moves possible from the adjacent tokens
  adjToklst= findAdjacentTok(playerDict, cell) 
  for adjTok in adjToklst:
    temp_move_lst= getSlides(adjTok, tokentype, playerDict, enemyDict, 1, cell)
    move_lst= move_lst + temp_move_lst
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
    player_tok= playerDict.get(coordinate_b)
    enemy_tok= playerDict.get(coordinate_b)
    #ensures the enemy_tok is of type list
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
    if  enemy_tok==None and coordinatesInBoundary(coordinate_b): ## if uppertok is the same
        movenode= [coordinate_a, coordinate_b, tok_type]
        unsorted_move_dict[0].append(movenode)
    return unsorted_move_dict


def minimax(playerDict, enemyDict, playerTeam, enemyTeam, playerMaxThrow, enemyMaxThrow, depth, maxdepth,  initialplayernumber, initialenemynumber, maximise=True):
    # check if we can return value
    return_val= eval(playerDict, enemyDict, depth, maxdepth, initialplayertokenseaten, initialenemytokenseaten)
    if return_val== "continue minimax":
        return return_val
    #else continute minimax process
    if maximise:
        bestval= float('-inf')
        for cell, tokenType in playerDict.items():
            slidesTemporary = getSlides(cell, tokenType, playerDict, enemyDict)
            swingsTemporary = getSwings(cell, tokenType, playerDict, enemyDict)
            throwsTemporary= getThrows(playerDict, enemyDict, playerTeam, self.self_throw_distance, self.current_turn)
            possibleMovelst= slidesTemporary + swingsTemporary + throwsTemporary
            for possibleMove in possibleMovelst:
                playerdictcopy= copy.deepcopy(playerDict)
                relocate_tokens(playerdictcopy, possibleMove)
                return minimax(playerdictcopy, enemyDict, playerTeam, enemyTeam, playerMaxThrow, enemyMaxThrow, depth+1, maxdepth, initialplayernumber, initialenemynumber, False)
            
    else:
        bestval= float('inf')
        for cell, tokenType in playerDict.items():
            slidesTemporary = getSlides(cell, tokenType, enemyDict, playerDict)
            swingsTemporary = getSwings(cell, tokenType, enemyDict, playerDict)
            throwsTemporary= getThrows(playerDict, enemyDict, playerTeam, self.self_throw_distance, self.current_turn)
            possibleMovelst= slidesTemporary + swingsTemporary + throwsTemporary
            for possibleMove in possibleMovelst:
                enemydictcopy= copy.deepcopy(enemyDict)
                relocate_tokens(enemydictcopy, possibleMove)
                return minimax(playerDict, enemydictcopy, playerTeam, enemyTeam, playerMaxThrow, enemyMaxThrow, depth+1, maxdepth, initialplayernumber, initialenemynumber)

            
            
def eval(playerDict, enemyDict, depth, maxdepth, initialplayernumber, initialenemynumber):
    #reached depth limit
    if depth==maxdepth:
        
        return 
    #a team got eaten
    elif len(playerDict)-initialplayernumber > 0:
        return 100
    elif len(enemyDict)-initialenemynumber > 0:
        return -100
    else:
        return "continue_minimax"
    
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
        
        # keeping track of how far the payer can throw a token
        self.self_throw_distance = 0
        
        # keeping track of how far the enemy can throw their token
        self.enemy_throw_distance = 0
        
          
    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        #if the game has just started, just randomly throw a piece on the board
        if self.current_turn==1:
            action= getThrows(self.selfdict, self.enemydict, self.team, self.self_throw_distance, True)
            return action
        
        action= None
        bestEval= float('-inf')
        #Traverse all team pieces on board, evaluate minimax eval for each possible move
        for cell, tokenType in self.selfdict.items():
            slidesTemporary = getSlides(cell, tokenType, self.selfdict, self.enemydict)
            swingsTemporary = getSwings(cell, tokenType, self.selfdict, self.enemydict)
            throwsTemporary= getThrows(self.selfdict, self.enemydict, self.team, self.self_throw_distance)
            possibleMovelst= slidesTemporary + swingsTemporary+ throwsTemporary
            for possibleMove in possibleMovelst:
                selfdictcopy= copy.deepcopy(self.selfdict)
                relocate_tokens(selfdictcopy, possibleMove)
                moveEval= minimax(selfdictcopy, self.enemydict, 0, 2, False, len(selfdictcopy), len(self.enemydict))
                if (moveEval > bestEval):
                    action = possibleMove
                    bestEval= moveEval
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
        
        self.current_turn = self.current_turn + 1
        
        #update throw distance
        if opponent_action[0] == "THROW":
          self.enemy_throw_distance = self.enemy_throw_distance + 1
        
        if player_action[0] == "THROW":
          self.self_throw_distance = self.self_throw_distance + 1
        
        ###  move the tokens for both teams
        relocate_tokens(self.enemydict, opponent_action)
        relocate_tokens(self.selfdict, player_action)
        
        
        ### see who has been eaten
        update_tokens_eaten(self.enemydict, self.selfdict)  ### function not implemented yet
        
        

      ######### OTHER HELPER FUNCTIONS
      ##############
    

          
    def update_tokens_eaten(dict1, dict2):
     # """ given two dictionaries, removes tokens in both dictionaries based on who gets eaten"""
      
      ### NOOOOOOTTEEEEEEE : MAYBE COUNT HOW MANY GETS EATEN
      
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


   
  
      

