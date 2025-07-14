import random
import sys
from os import system

#set number of piles for game
piles = 7
#set number of cards to draw each turn
global draw
draw = 3
#Define card suits & numbers
suits = ['♠', '♣', '♥', '♦']
values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']


class Card:
#initialise card class
    def __init__(self, value, suit):
        self.suit = suit
        self.value = value
        self.colour = 0
        if self.suit in ['♥', '♦']:
            self.colour = 1
        self.visible = False

#turn card over
    def turn (self):
        if self.visible :
            self.visible == False
        else:
            self.visible == True

#return card as f string
    def __str__(self):
        if self.visible:
            return f"{self.value}{self.suit}"
        else:
            return("##")


#create deck/pile containing cards
class Deck:
    def __init__(self):
        self.cards = []
        self.count = 0

#create a shuffled deck with cards from values & suits
    def new(self):
        for x in values:
            for s in suits:
                card = Card(x, s)
                self.add(card)
        self.shuffle()

#add card to deck/pile
    def add (self, card):
        self.cards.append(card)
        self.count += 1

#remove card from deck/pile
    def draw(self):
        #check if deck has cards
        if self.count < 1 :
            return False
        else:
            self.count -= 1
            return self.cards.pop()

#shuffle deck
    def shuffle(self):
        random.shuffle(self.cards)

#turn all cards in deck over
    def turn_all(self):
        for card in self.cards:
            card.visible = False

#print deck/pile print ## if not yet turned
    def __str__(self):
        cards = []
        for card in self.cards:
            cards.append(f"{card}")
#for line in range(piles):
        return f"{cards}"

#deal from a deck into a dictionary with n lists of cards
    def deal(self, n):
        deal = {}
        for x in range(n):
            pile = Deck()
            for y in range((x + 1)):
                pile.add(self.draw())
                if y == x:
                    pile.cards[y].visible = True
            deal[x] = pile
        return deal

def printInstructions():
    return(
        f"+------------------------------------------------+\n"
        f"|                Instructions                    |\n"
        f"+------------------------------------------------+\n"
        f"|           Moves                                |\n"
        f"| d - Draw cards                                 |\n"
        f"| 1 to 7 - move drawn card to pile number        |\n"
        f"| m - move card(s) between piles follow prompts  |\n"
        f"| p - promote drawn card to aces piles           |\n"
        f"| p1-7 - promote card from pile to aces piles    |\n"
        f"| c - change number of cards drawn               |\n"
        f"| r - restart game                               |\n"
        f"| x - Exit game                                  |\n"
        f"+------------------------------------------------+\n"
    )
#print cards for current game
def print_piles(game, aces):
    system('clear')
    print(printInstructions())
#print pile headers
    print("\u03321____\u03322____\u03323____\u03324____\u03325____\u03326____\u03327    H♥   S♠   C♣   D♦")
#variable to track size of largest pile
    largest = 0
#find size of largest pile
    for pile in game.values():
        if len(pile.cards) > largest:
            largest = len(pile.cards)
#print cards line by line
    for x in range(largest):
        for y in range(piles):
#check if current pile has cards left to turn, if not print blank space
            if x >= len(game[y].cards):
                print("  ", end='   ' )
            else:
#if cards available to print, check if the card is visible and a 10 to apply special formating
                if game[y].cards[x].visible == True and game[y].cards[x].value == '10':
                    print(game[y].cards[x], end = '  ')
#print card no special spacing
                else:
                    print(game[y].cards[x], end = '   ')
#print aces
        if y == 6 and x == 0:
            blank = "  "
            print(f"{(aces['♥'].cards or blank)[-1]}    {(aces['♠'].cards or blank)[-1]}    {(aces['♣'].cards or blank)[-1]}    {(aces['♦'].cards or blank)[-1]}", end="")
#new line
        print()



class Game:
    def __init__(self, deck):
        self.deck = deck
        self.discard = Deck()
        self.aces = {}
        for s in suits:
            self.aces[s] = Deck()
        self.game = self.deck.deal(piles)


    #def check_move(self, pile, card):
    #    try:
    #        if card.value == "K" and len(pile.cards) == 0:
    #            return True
    #        elif pile.cards[-1].colour != card.colour and pile.count > 0:
    #            if (values.index(pile.cards[-1].value) - 1) == values.index(card.value) :
    #                return True
    #        else:
    #            return False
    #    except IndexError:
    #        pass
    #def check_promote(self, card):

    #    if card.value == 'A':
    #        return True
    #    elif len(self.aces[card.suit].cards) > 0:
    #        if (values.index(self.aces[card.suit].cards[-1].value) + 1) == values.index(card.value) :
    #            return True
    def move(self, move):
        global new_game
        match move:
            case 'x':
                sys.exit(1)
            case 'd':
                global draw
                for x in range(draw):
                    card = self.deck.draw()
                    if card:
                        card.visible = True
                        self.discard.add(card)
                        print_piles(self.game, self.aces)
                        print(card)
                    else:
                        self.deck = self.discard
                        self.deck.turn_all()
                        self.discard = Deck()
                        print_piles(self.game, self.aces)
                        print(f"##")

            case '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7':
                if self.discard.count > 0:
                    pile = int(move) - 1
                    if check_move(self.game[pile], self.discard.cards[-1]):
                            self.game[pile].add(self.discard.draw())
                print_piles(self.game, self.aces)
                if self.discard.count > 0:
                    print(self.discard.cards[-1])
                else:
                    print("##")
            case 'p'|'p0'|'p1'|'p2'|'p3'|'p4'|'p5'|'p6'|'p7':
                if move == 'p':
                    if self.discard.count > 0:
                        if check_promote(self, self.discard.cards[-1]):
                            self.aces[self.discard.cards[-1].suit].add(self.discard.draw())
                        print_piles(self.game,self.aces)
                    if self.discard.count > 0:
                        print(self.discard.cards[-1])
                    else:
                        print("##")
                else:
                    pile = int(move[1]) - 1
                    if check_promote(self, self.game[pile].cards[-1]):
                        self.aces[self.game[pile].cards[-1].suit].add(self.game[pile].draw())
                        if len(self.game[pile].cards) > 0:
                            self.game[pile].cards[-1].visible = True
                    print_piles(self.game,self.aces)
                    if self.discard.count > 0:
                        print(self.discard.cards[-1])
                    else:
                        print("##")
            case 'm':
                try:
                    pile_from = int(input("From pile: "))-1
                    cards = int(input("Number of cards: "))
                    pile_to = int(input("To pile: "))-1
                    if cards == 1:
                        if check_move(self.game[pile_to], self.game[pile_from].cards[-1]):
                            self.game[pile_to].add(self.game[pile_from].draw())
                            if len(self.game[pile_from].cards) > 0:
                                self.game[pile_from].cards[-1].visible = True
                        if self.discard.count > 0:
                            print(self.discard.cards[-1])
                    ##Moving a group of cards
                    elif cards > 1:
                        group = self.game[pile_from].cards[(cards*-1):]
                        if check_move(self.game[pile_to], group[0]):
                            for card in group:
                                print(card)
                                self.game[pile_to].add(card)
                                self.game[pile_from].draw()
                            if len(self.game[pile_from].cards) > 0:
                                self.game[pile_from].cards[-1].visible = True
                except ValueError:
                    print("Only enter numbers!")
                    pass
                print_piles(self.game,self.aces)
                if self.discard.count > 0:
                        print(self.discard.cards[-1])
            case 'r':
                system('clear')
                main()
            case 'c':
                draw = int(input("New draw count: "))

def check_win (aces):
    win = False
    try:
        for pile in aces:
            if aces[pile].cards[-1].value == "K":
                win = True
            else:
                break
        return win
    except IndexError:
        pass

def check_move(pile, card):
        try:
            if card.value == "K" and len(pile.cards) == 0:
                return True
            elif pile.cards[-1].colour != card.colour and pile.count > 0:
                if (values.index(pile.cards[-1].value) - 1) == values.index(card.value) :
                    return True
            else:
                return False
        except IndexError:
            pass
def check_promote(self, card):

    if card.value == 'A':
        return True
    elif len(self.aces[card.suit].cards) > 0:
        if (values.index(self.aces[card.suit].cards[-1].value) + 1) == values.index(card.value) :
            return True

def main():
    new_deck = Deck()
    new_deck.new()
    new_game = Game(new_deck)
    print_piles(new_game.game, new_game.aces)
    for x in range(draw):
        card = new_game.deck.draw()
        if card:
            card.visible = True
            new_game.discard.add(card)
        else:
            new_game.deck = discard
            new_game.deck.turn_all()
            print("##")
            new_game.discard = Deck()
    print(card)
    while True:
#check if game has been won
        if check_win(new_game.aces):
            print("CONGRATULATIONS GAME COMPLETE!!")
            print("Type r to restart or x to Exit")
            action = input("Action : ")
            if action == "r":
                system('clear')
                main()
            elif action == "x":
                sys.exit(1)
        else:
#prompt user for a move
            new_game.move(input("Move :"))

#def move(move):
#    global main_deck, aces, discard, game





if __name__ == "__main__" :
    main()





