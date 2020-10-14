import math

C = 1


class Node:
    def __init__(self, parent, prior_p, action, player, game):
        self.parent = parent  # parent node
        self.action = action  # corresponding action
        self.player = player  # 1 for black -1 for white
        self.children = {}  # a map from action to Node
        self.n_visits = 0  # number of time visited
        self.Q = 0  # total value received
        self.ucb = 0  # UCB value
        self.P = prior_p  # prior probability
        self.game = game  # game function
        self.is_game_over_node = False

    def get_state(self):
        if self.action is None:
            return self.game.get_empty_board()
        else:
            parent_state = self.parent.get_state()
            parent_state[self.action] = self.player
            return parent_state

    def select(self):
        if self.children == {}:
            return self
        else:
            max_ucb = 0
            max_ucb_action = None
            for action in self.children:
                ucb = self.children[action].ucb
                if ucb >= max_ucb:
                    max_ucb = ucb
                    max_ucb_action = action

            # move to the selected node
            return self.children[max_ucb_action].select()

    def expand(self, prior_p):
        # initialize children and calculate their UCB value
        for action in prior_p:
            self.children[action] = Node(parent=self,
                                         prior_p=prior_p[action],
                                         action=action,
                                         player=-1 if self.player == 1 else 1,
                                         game=self.game)
            self.children[action].ucb = C * prior_p[action] * math.sqrt(self.n_visits)

    def back_propagate(self, value):
        self.Q += value  # TODO:Will value of Q overflow???
        self.n_visits += 1
        self.ucb = self.Q / self.n_visits + C * self.P * math.sqrt(self.parent.n_visits) / (1 + self.n_visits)
        if self.parent is not None:
            self.parent.backpropagation(-value)


class MCTS:
    def __init__(self, game, policy_value_fn, c_uct, n_playout):
        self.game = game
        self.policy = policy_value_fn
        self.root = Node(None, 1.0, None, 1, game)
        self.c_uct = c_uct
        self.n_playout = n_playout

        self.game_node = self.root

    def selection(self):
        """
        the second kind of implementation
        """
        return self.game_node.select()

    def expansion(self, node):
        node_state = node.get_state()
        # if current node is a game over node, skip expansion, return reward
        if self.game.check_if_game_ends(player=node.player,
                                        row=node.action[0],
                                        col=node.action[1],
                                        board=node_state):
            # TODO:有一个小问题，这个node是game over node，假设player是1，则winner是上一层的2
            return node.player

        available_action = self.game.get_available_action(node_state)
        # TODO: corresponding function will be added later
        prior_p, value = self.policy.evaluate(node_state, available_action)
        node.expand(prior_p)
        return value

    @staticmethod
    def back_propagate(node, value):
        node.backpropagation(value)

    def start_exploring(self):
        for i in range(self.n_playout):
            selected_node = self.selection()
            value = self.expansion(selected_node)
            self.back_propagate(selected_node, value)

# Consider replace 1,2 with -1 and 1 for player 1 and 2
# The part of finding action with the maximum UCB value can be optimized
