from spade import agent, quit_spade, behaviour
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import time

X = int(os.getenv('X'))
Y = int(os.getenv('Y'))
STEPS = int(os.getenv('STEPS'))


class SquareAgent(agent.Agent):

    def __init__(self, jid, password, isAlive=False):
        super().__init__(jid, password)
        self.isAlive = isAlive
        self.neighbourhood = []

    def setupNeighbourhood(self, neighbours):
        self.neighbourhood = neighbours

    async def setup(self):
        b = self.NextLife(self.neighbourhood)
        self.add_behaviour(b)

    class NextLife(behaviour.OneShotBehaviour):
        def __init__(self, neighbourhood):
            super().__init__()
            self.neighbourhood = neighbourhood

        async def run(self):
            aliveCount = 0
            for agent in self.neighbourhood:
                if (agent.isAlive):
                    aliveCount += 1

            if (aliveCount == 3 and not self.agent.isAlive):
                self.agent.isAlive = True
            elif (aliveCount == 2 or aliveCount == 3) and self.agent.isAlive:
                self.agent.isAlive = True
            else:
                self.agent.isAlive = False


def update(frameNum, frames, im):
    im.set_data(frames[frameNum])
    return im


class BoardAgent(agent.Agent):
    def __init__(self, jid, password, xSize=20, ySize=20, steps=10):
        super().__init__(jid, password)
        self.xSize = xSize
        self.ySize = ySize
        self.board = []
        self.steps = steps
        for col in range(xSize):
            row = []
            for r in range(ySize):
                if random.random() <= 0.5:
                    row.append(SquareAgent(jid, password, True))
                else:
                    row.append(SquareAgent(jid, password, False))
            self.board.append(row)

    async def setup(self):
        for col in range(1, self.xSize - 1):
            for row in range(1, self.ySize - 1):
                neighbours = [self.board[col - 1][row - 1], self.board[col][row - 1], self.board[col + 1][row - 1],
                              self.board[col - 1][row], self.board[col + 1][row], self.board[col - 1][row + 1],
                              self.board[col][row + 1], self.board[col + 1][row + 1]]
                self.board[col][row].setupNeighbourhood(neighbours)
        frames = []
        for i in range(self.steps):
            print("STEP: {}".format(i + 1))
            grid = []
            for col in range(board.xSize):
                r = []
                for row in range(board.ySize):
                    await self.board[col][row].start(False)
                    # await self.board[col][row].stop()
                    # await self.board[col][row].result()
                    r.append(255 if (self.board[col][row].isAlive) else 0)
                    # await self.board[col][row].stop()
                grid.append(r)
            frames.append(grid)

        # Config
        fig, ax = plt.subplots(figsize=(12, 12))
        plt.axis('off')
        fig.set_tight_layout(True)
        image = ax.imshow(frames[0])

        anim = FuncAnimation(fig, update, frames=self.steps, fargs=[frames, image])
        anim.save('life.gif', dpi=80, writer='imagemagick')
        # isAnyStillRunning = True
        # while isAnyStillRunning:
        #     for col in range(self.xSize):
        #         isAnyStillRunning = False
        #         for row in range(self.ySize):
        #             if (self.board[col][row].is_alive()):
        #                 isAnyStillRunning = True
        #                 break
        #         if (isAnyStillRunning):
        #             break
        #     time.sleep(0.1)


print("Starting with options: X: {}, Y: {}, STEPS: {}".format(X, Y, STEPS))
board = BoardAgent("admin@localhost", "polska1", X, Y, STEPS)
future = board.start()
future.result()
board.stop()
quit_spade()
