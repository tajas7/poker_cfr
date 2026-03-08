class Node():

    def __init__(self, actions):
        self.actions = actions
        self.cumulative_regret = dict()
        self.strategy = dict()
        self.cumulative_strategy = dict()

        for action in actions:
            self.cumulative_regret[action] = 0.0
            self.strategy[action] = 0.0
            self.cumulative_strategy[action] = 0.0

    def get_strategy(self, realization_weight):
        normalization_sum = 0

        for action in self.actions:
            self.strategy[action] = self.cumulative_regret[action] if self.cumulative_regret[action] > 0 else 0
            normalization_sum += self.strategy[action]

        for action in self.actions:
            if normalization_sum > 0:
                self.strategy[action] /= normalization_sum
            else:
                self.strategy[action] = 1.0 / len(self.actions)
            self.cumulative_strategy[action] += realization_weight * self.strategy[action]

        return self.strategy

    def get_average_strategy(self):
        average_strategy = dict()
        normalization_sum = 0

        for action in self.actions:
            normalization_sum += self.cumulative_strategy[action]

        for action in self.actions:
            if normalization_sum > 0:
                average_strategy[action] = self.cumulative_strategy[action] / normalization_sum
            else:
                average_strategy[action] = 1.0 / len(self.actions)

        return average_strategy
