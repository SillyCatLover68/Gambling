import random
import time

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10,
          'Ace': 11}
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank


def take_bet(chips):
    while True:
        try:
            bet = int(input(f"You have {chips} chips. How much would you like to bet? "))
            if bet > 0 and bet <= chips:
                return bet
            else:
                print("Bet must be a positive integer within your chip range!")
        except ValueError:
            print("Bet must be a positive integer!")


def hit(deck, hand):
    hand.add_card(deck.deal())


def hit_or_stand(deck, hand):
    global playing
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's': ")
        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False
        else:
            print("Invalid input. Please enter 'h' or 's' only.")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    time.sleep(1)
    print(" <hidden card>")
    time.sleep(1)
    print('', dealer.cards[1])
    time.sleep(1)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    time.sleep(1)


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    time.sleep(1)
    print("Dealer's Hand =", dealer.value)
    time.sleep(1)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    time.sleep(1)
    print("Player's Hand =", player.value)
    time.sleep(1)


def player_busts(chips, bet):
    print("Player busts!")
    time.sleep(1)
    return chips - bet


def player_wins(chips, bet):
    print("Player wins!")
    time.sleep(1)
    return chips + bet


def dealer_busts(chips, bet):
    print("Dealer busts!")
    time.sleep(1)
    return chips + bet


def dealer_wins(chips, bet):
    print("Dealer wins!")
    time.sleep(1)
    return chips - bet


def push():
    print("Dealer and Player tie! It's a push.")
    time.sleep(1)

playing = True
player_chips = 100

while True:
    print("Welcome to Blackjack!")
    time.sleep(1)

    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Prompt the player for their bet
    bet = take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    if player_hand.can_split():
        split = input("You can split your hand. Would you like to split? Enter 'y' or 'n': ")
        if split[0].lower() == 'y':
            # Create second hand
            hand1 = Hand()
            hand2 = Hand()
            hand1.add_card(player_hand.cards[0])
            hand2.add_card(player_hand.cards[1])

            # Deal one more card to each hand
            hand1.add_card(deck.deal())
            hand2.add_card(deck.deal())

            for i, hand in enumerate([hand1, hand2], 1):
                playing = True
                print(f"\nPlaying Hand {i}:")
                time.sleep(1)
                show_some(hand, dealer_hand)
                while playing:
                    hit_or_stand(deck, hand)
                    show_some(hand, dealer_hand)
                    if hand.value > 21:
                        player_chips = player_busts(player_chips, bet)
                        break

                if hand.value <= 21:
                    while dealer_hand.value < 17:
                        hit(deck, dealer_hand)
                    show_all(hand, dealer_hand)
                    if dealer_hand.value > 21:
                        player_chips = dealer_busts(player_chips, bet)
                    elif dealer_hand.value > hand.value:
                        player_chips = dealer_wins(player_chips, bet)
                    elif dealer_hand.value < hand.value:
                        player_chips = player_wins(player_chips, bet)
                    else:
                        push()

            continue

    while playing:
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_chips = player_busts(player_chips, bet)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        show_all(player_hand, dealer_hand)
        if dealer_hand.value > 21:
            player_chips = dealer_busts(player_chips, bet)
        elif dealer_hand.value > player_hand.value:
            player_chips = dealer_wins(player_chips, bet)
        elif dealer_hand.value < player_hand.value:
            player_chips = player_wins(player_chips, bet)
        else:
            push()

    print("\nPlayer's chips:", player_chips)
    time.sleep(1)

    new_game = input("Would you like to play another hand? Enter 'y' or 'n': ")
    if new_game[0].lower() == 'n':
        print("Thanks for playing!")
        break
    else:
        playing = True
