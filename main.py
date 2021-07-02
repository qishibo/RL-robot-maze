import time
from Layout import InitLayout
from Agent import Agent

 
def start():
    # 总迭代次数
    TOTAL_EXPLORE_EPOCH = 400
    # 95%迭代后开始查看效果
    SHOW_SLOW_EFFECT = TOTAL_EXPLORE_EPOCH * 0.95

    for epoc in range(TOTAL_EXPLORE_EPOCH):
        # 智能体初始坐标
        observation = env.reset()
        # 每次迭代结束时的总分数
        total_reward = 0

        while True:
            env.render()
            action = MyAgent.action_select(str(observation))
            # 移动，并获取reward
            next_observation, reward, done = env.step(action)
            # 更新qtable
            MyAgent.update_q_table(str(observation), action, reward, str(next_observation))
            observation = next_observation

            # 结果慢动作展示
            if epoc > SHOW_SLOW_EFFECT:
                time.sleep(0.2)
            # 总分叠加
            total_reward = total_reward + reward

            if done:
                print('==== epoch %d R: %.6f ====' %(epoc, total_reward))
                break
    MyAgent.q_table.to_csv("Qtable.csv")
    env.destroy()

if __name__ == "__main__":
    # 初始化幕布
    env = InitLayout()
    MyAgent = Agent(actions=range(env.actions_num))
    env.after(10, start)
    # 开始主循环
    env.mainloop()
