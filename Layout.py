import numpy as np
import tkinter as tk

class InitLayout(tk.Tk):
    # gridNum格子数 gridWidth每个格子宽度 objWidth里面物体的宽度
    def __init__(self, gridNum = 5, gridWidth = 80, objWidth = 50):
        super(InitLayout, self).__init__()
        self.title('机器人走迷宫')
        self.gridNum = gridNum
        self.gridWidth = gridWidth
        self.objWidth = objWidth
        self.borderSize = self.gridNum * self.gridWidth
        # 4种action
        self.action_space = ['up', 'down', 'left', 'right']
        self.actions_num = len(self.action_space)
        # 黑洞位置, 为行列格子数的索引
        self.blacks = [[0, 2], [1, 2], [2, 4], [3, 0], [3, 1], [3, 4], [4, 4], [4, 2]]
        # 黑洞坐标集合
        self.blackCoors = []
        self.start_drawing()
 
    def start_drawing(self):
        # 初始化
        self.drawing = tk.Canvas(self, height=self.borderSize, width=self.borderSize, bg='#c9ccd0')
        # 画线
        for col in range(0, self.borderSize, self.gridWidth):
            x0, y0, x1, y1 =col, 0, col, self.borderSize
            self.drawing.create_line(x0, y0, x1, y1)
        for row in range(0, self.borderSize, self.gridWidth):
            x0, y0, x1, y1 = 0, row, self.borderSize , row
            self.drawing.create_line(x0, y0, x1, y1)
 
        # 初始基点
        start_pos = np.array([self.gridWidth / 2, self.gridWidth / 2])

        # 循环画黑洞
        for index, pos_tup in enumerate(self.blacks):
            col, row = pos_tup
            center_pos = start_pos + np.array([self.gridWidth * col, self.gridWidth * row])
            hell = self.drawing.create_oval(
                center_pos[0] - self.objWidth / 2, center_pos[1] - self.objWidth / 2,
                center_pos[0] + self.objWidth / 2, center_pos[1] + self.objWidth / 2,
                fill='black')
            # 追加倒黑洞坐标中
            self.blackCoors.append(self.drawing.coords(hell))
         
        # 画终点
        dist_center = start_pos + np.array([self.gridWidth * 4, self.gridWidth * 2])
        self.dist = self.drawing.create_oval(
            dist_center[0] - self.objWidth / 2, dist_center[1] - self.objWidth / 2,
            dist_center[0] + self.objWidth / 2, dist_center[1] + self.objWidth / 2,
            fill='yellow')
 
        # 画智能体
        self.rect = self.drawing.create_oval(
            start_pos[0] - self.objWidth / 2, start_pos[1] - self.objWidth / 2,
            start_pos[0] + self.objWidth / 2, start_pos[1] + self.objWidth / 2,
            fill='#4ed660')
 
        self.drawing.pack()
 
    def reset(self):
        # 重新画智能体位置
        self.drawing.delete(self.rect)
        origin = np.array([self.gridWidth / 2, self.gridWidth / 2])
        self.rect = self.drawing.create_oval(
            origin[0] - self.objWidth / 2, origin[1] - self.objWidth / 2,
            origin[0] + self.objWidth / 2, origin[1] + self.objWidth / 2,
            fill='#4ed660')

        return self.drawing.coords(self.rect)

    # 智能体移动
    def step(self, action):
        s = self.drawing.coords(self.rect)
        agent_pos = np.array([0, 0])
        # 进行移动位置
        if action == 0: # up
            if s[1] > self.gridWidth:
                agent_pos[1] -= self.gridWidth
        elif action == 1: # down
            if s[1] < (self.gridNum - 1) * self.gridWidth:
                agent_pos[1] += self.gridWidth
        elif action == 2: # left
            if s[0] > self.gridWidth:
                agent_pos[0] -= self.gridWidth
        elif action == 3: # right
            if s[0] < (self.gridNum - 1) * self.gridWidth:
                agent_pos[0] += self.gridWidth


        # 移动图形
        self.drawing.move(self.rect, agent_pos[0], agent_pos[1])
        sig = self.drawing.coords(self.rect)
 
        # 到达终点
        if sig == self.drawing.coords(self.dist):
            reward = 100
            finished = True
            sig = 'finished'
        # 掉入黑洞
        elif sig in self.blackCoors:
            reward = -100
            finished = True
            sig = 'finished'
        else:
            reward = -1
            finished = False
 
        return sig, reward, finished
 
    def render(self):
        self.update()
