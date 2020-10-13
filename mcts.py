import math

C = 1


class Node:
    def __init__(self, parent, prior_p, action, player, game):
        self.parent = parent  # parent node
        self.action = action  # corresponding action
        self.player = player  # 1 for black 2 for white
        self.children = {}  # a map from action to Node
        self.n_visits = 0  # number of time visited
        self.Q = 0  # total value received
        self.ucb = 0  # UCB value
        self.P = prior_p  # prior probability
        self.game = game  # game function
        self.is_game_over_node = False

    def init_node(self):
        pass

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
            max_ucb_child = None
            for child_key in self.children:
                ucb = self.children[child_key].ucb
                if ucb >= max_ucb:
                    max_ucb = ucb
                    max_ucb_child = child_key

            # move to the selected node
            self.children[max_ucb_child].select()

    def expand(self, prior_p, value):
        for action in prior_p:
            self.children[action] = Node(parent=self,
                                         prior_p=prior_p[action],
                                         action=action,
                                         player=2 if self.player == 1 else 1,
                                         game=self.game)

    def backpropagation(self, value):
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
        from current state (self.game_node)
        keep on choosing node (based on UCB value)
        until an unexpanded node is encountered.
        """
        current_node = self.game_node  # node of each selection step
        while True:
            # select child node with maximum UCB value
            max_ucb = 0
            max_ucb_child = None
            for child_key in current_node.children:
                ucb = current_node.children[child_key].ucb
                if ucb >= max_ucb:
                    max_ucb = ucb
                    max_ucb_child = child_key

            # move to the selected node
            current_node = current_node.children[max_ucb_child]

            # end selection process when node is not expanded (leaf node)
            if current_node.children == {}:
                return current_node

    def selection_2(self):
        """
        the second kind of implementation
        """
        return self.game_node.select()

    def expansion(self, node):
        # TODO: what if the selected node is a game over node
        node_state = node.get_state()
        if self.game.check_if_game_ends(player=node.player,
                                        row=node.action[0],
                                        col=node.action[1],
                                        board=node_state):
            return node.player

        available_action = self.game.get_available_action(node_state)
        # TODO: corresponding function will be added later
        prior_p, value = self.policy.evaluate(node_state, available_action)
        node.expand(prior_p, value)

    def backpropagation(self):
        pass
