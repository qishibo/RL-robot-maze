import numpy as np
import pandas as pd


class Agent:
    # learning_rate学习率 reward_decay折扣率 epsilon e贪婪系数
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, epsilon=0.01):
        self.lr = learning_rate
        self.gamma = reward_decay
        self.actions = actions
        self.epsilon = epsilon
        # qtable分数表
        self.q_table = pd.DataFrame(columns=self.actions)

    def update_q_table(self, s, a, r, sig):
        self.check_in_qtable(sig)
        # 获取当前qtable值
        q_value = self.q_table.loc[s, a]
        if sig != 'finished':
            q_target = r + self.gamma * self.q_table.loc[sig, :].max()
        else:
            q_target = r
        # 更新qtable
        self.q_table.loc[s, a] += self.lr * (q_target - q_value)

    def action_select(self, observation):
        self.check_in_qtable(observation)
        # e贪婪策略，大于e取最高reward
        if np.random.uniform() > self.epsilon:
            state_action = self.q_table.loc[observation, :]
            # np.max(state_action) 为下一个state行中最大的一列，即最大分数的action
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # 命中随机策略
            action = np.random.choice(self.actions)

        print("selected action: ", ['up', 'down', 'left', 'right'][action])
        return action

    def check_in_qtable(self, state):
        # 不在则添加
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    name=state,
                    index=self.q_table.columns
                )
            )
