from Node import Node


class CFR():

    def __init__(self, game):
        self.node_map = dict()
        self.game = game

    def train(self, iterations):
        utility = 0.0

        for i in range(iterations):
            player1_cards, player2_cards = self.game.deal_cards()
            player1_hand = self.game.hand_representation(player1_cards)
            player2_hand = self.game.hand_representation(player2_cards)

            hands = [player1_hand, player2_hand]
            history = []
            utility += self.cfr(hands, history, 1, 1)

        return utility / iterations

    def get_strategy(self):
        result = dict()
        player1_bet = "P1 bets"
        player1_bet_call = "P1 calls"
        player1_check_call = "P1 check-call"
        player1_check_raise = "P1 check-raise"

        result[player1_bet] = dict()
        result[player1_bet_call] = dict()
        result[player1_check_call] = dict()
        result[player1_check_raise] = dict()

        player2_call = "P2 calls"
        player2_raise = "P2 raises"
        player2_bet = "P2 bets"
        player2_bet_call = "P2 bet-call"

        result[player2_call] = dict()
        result[player2_raise] = dict()
        result[player2_bet] = dict()
        result[player2_bet_call] = dict()

        for state, node in self.node_map.items():
            hand = state[0:2] if state[0] == state[1] else state[0:3]
            history = state[2:] if len(hand) == 2 else state[3:]

            # P1
            if len(history) == 0:
                result[player1_bet][hand] = node.strategy[self.game.bet()]
            # P2
            elif len(history) == 1:
                if history[0] == self.game.check():
                    result[player2_bet][hand] = node.strategy[self.game.bet()]
                else:
                    result[player2_raise][hand] = node.strategy[self.game.bet()]
                    result[player2_call][hand] = node.strategy[self.game.call()]
            # P1
            elif len(history) == 2:
                if history[0] == self.game.bet():
                    result[player1_bet_call][hand] = node.strategy[self.game.call()]
                else:
                    result[player1_check_raise][hand] = node.strategy[self.game.bet()]
                    result[player1_check_call][hand] = node.strategy[self.game.call()]
            # P2
            elif len(history) == 3:
                result[player2_bet_call][hand] = node.strategy[self.game.call()]

        return result

    def cfr(self, hands, history, prob1, prob2):
        num_actions = len(history)
        player = num_actions % 2
        opponent = 1 - player
        player_hand = hands[player]
        opponent_hand = hands[opponent]

        realization_weight = prob1 if player == 0 else prob2

        if num_actions >= 2:

            if history[-1] == self.game.fold():
                num_bets = 0
                for action in history:
                    if action == self.game.bet():
                        num_bets += 1

                if num_bets == 2:
                    return self.game.ante + self.game.bet1

                return self.game.ante

            if history[-1] == self.game.call():
                winner = self.game.best_hand(player_hand, opponent_hand)
                if winner == 0:
                    return 0

                reward = self.game.ante
                num_bets = 0
                for action in history:
                    if action == self.game.bet():
                        num_bets += 1
                if num_bets == 2:
                    reward += self.game.bet2
                elif num_bets == 1:
                    reward += self.game.bet1
                return reward if winner == 1 else -reward

            if history[-1] == self.game.check():
                winner = self.game.best_hand(player_hand, opponent_hand)
                if winner == 0:
                    return 0
                return self.game.ante if winner == 1 else -self.game.ante

        state = str(player_hand)
        for action in history:
            state += action

        if state in self.node_map:
            node = self.node_map[state]
            possible_actions = node.actions
        else:
            if len(history) == 0:
                possible_actions = [self.game.check(), self.game.bet()]
            else:
                if history[-1] == self.game.bet():
                    possible_actions = [self.game.call(), self.game.fold()]

                    num_bets = 0
                    for action in history:
                        if action == self.game.bet():
                            num_bets += 1

                    if num_bets == 1:
                        possible_actions.append(self.game.bet())
                else:
                    possible_actions = [self.game.check(), self.game.bet()]

            node = Node(possible_actions)
            self.node_map[state] = node

        strategy = node.get_strategy(realization_weight)
        utility = dict()
        node_utility = 0

        for action in possible_actions:
            next_history = list(history)
            next_history.append(action)

            if player == 0:
                utility[action] = -self.cfr(hands, next_history, prob1 * strategy[action], prob2)
            else:
                utility[action] = -self.cfr(hands, next_history, prob1, prob2 * strategy[action])

            node_utility += strategy[action] * utility[action]

        for action in possible_actions:
            regret = utility[action] - node_utility
            if player == 0:
                node.cumulative_regret[action] += regret * prob2
            else:
                node.cumulative_regret[action] += regret * prob1

        return node_utility
