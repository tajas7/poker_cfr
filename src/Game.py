import random


class Game():
    def __init__(self, ante=1.0, bet1=2.0, bet2=8.0):
        self.ante = ante
        self.bet1 = bet1
        self.bet2 = bet2
        self.ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        self.suits = ['s', 'c', 'd', 'h']
        self.deck = [rank + suit for rank in self.ranks for suit in self.suits]

    def reset_deck(self):
        self.deck = [rank + suit for rank in self.ranks for suit in self.suits]
        random.shuffle(self.deck)

    def deal_cards(self):
        self.reset_deck()
        cards = random.sample(self.deck, 4)
        player1_hand = cards[0:2]
        player2_hand = cards[2:]

        return player1_hand, player2_hand

    def hand_representation(self, hand):
        rank1 = hand[0][0]
        suit1 = hand[0][1]
        rank2 = hand[1][0]
        suit2 = hand[1][1]

        if rank1 == rank2:
            return rank1 + rank2

        hand = self.higher_rank(rank1, rank2)
        hand += rank2 if hand == rank1 else rank1
        hand += 's' if suit1 == suit2 else 'o'

        return hand

    def higher_rank(self, rank1, rank2):
        for rank in self.ranks:
            if rank1 == rank:
                return rank1
            if rank2 == rank:
                return rank2
        return rank1

    def best_hand(self, hand1, hand2):
        is_pair_hand1 = hand1[0] == hand1[1]
        is_pair_hand2 = hand2[0] == hand2[1]

        if is_pair_hand1 and is_pair_hand2:
            if hand1[0] == hand2[0]:
                return 0
            if hand1[0] == self.higher_rank(hand1[0], hand2[0]):
                return 1
            else:
                return 2
        elif is_pair_hand1 and not is_pair_hand2:
            return 1
        elif is_pair_hand2 and not is_pair_hand1:
            return 2

        is_suited_hand1 = hand1[2] == 's'
        is_suited_hand2 = hand2[2] == 's'

        if is_suited_hand1 and is_suited_hand2:
            if hand1[0] == hand2[0]:
                if hand1[1] == hand2[1]:
                    return 0
                elif hand1[1] == self.higher_rank(hand1[1], hand2[1]):
                    return 1
                return 2
            if hand1[0] == self.higher_rank(hand1[0], hand2[0]):
                return 1
            else:
                return 2
        elif is_suited_hand1 and not is_suited_hand2:
            return 1
        elif is_suited_hand2 and not is_suited_hand1:
            return 2

        if hand1[0] == hand2[0]:
            if hand1[1] == hand2[1]:
                return 0
            if hand1[1] == self.higher_rank(hand1[1], hand2[1]):
                return 1
            return 2
        if hand1[0] == self.higher_rank(hand1[0], hand2[0]):
            return 1
        else:
            return 2

    def bet(self):
        return '0'

    def call(self):
        return '1'

    def check(self):
        return '2'

    def fold(self):
        return '3'
