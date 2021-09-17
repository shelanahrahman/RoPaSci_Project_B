
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
        #testing throw action
        if  self.team=="upper":
            start=4
        else:
            start=-4
            
        if self.current_turn==1:
            return "THROW", "s", (start, 0)
        # testing slide action
        else:
            if self.team=="upper":
                return "SLIDE", list(self.selfdict)[0], (list(self.selfdict)[0][0]-1,list(self.selfdict)[0][1]+1)
            else:
                return "SLIDE", list(self.selfdict)[0], (list(self.selfdict)[0][0]+1,list(self.selfdict)[0][1]-1)
    
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


   
  
      

