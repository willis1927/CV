from project import check_move,check_win,printInstructions, Deck, Card, Game

def main():
    test_check_win()
    test_check_promote()
  #  test_check_move()


def test_check_win():
    suits = ['♠', '♣', '♥', '♦']
    aces = {}
    for s in suits:
        aces[s] = Deck()
        card = Card('K',s)
        aces[s].add(card)
    assert check_win(aces) == True

def test_printInstructions():
    assert printInstructions() == "+------------------------------------------------+\n|                Instructions                    |\n+------------------------------------------------+\n|           Moves                                |\n| d - Draw cards                                 |\n| 1 to 7 - move drawn card to pile number        |\n| m - move card(s) between piles follow prompts  |\n| p - promote drawn card to aces piles           |\n| p1-7 - promote card from pile to aces piles    |\n| c - change number of cards drawn               |\n| r - restart game                               |\n| x - Exit game                                  |\n+------------------------------------------------+\n"

def test_check_move():
    card = Card('K','♠')
    pile = Deck()
    assert check_move(pile, card) == True



#def test_check_move():






if __name__ == "__main__":
    main()
