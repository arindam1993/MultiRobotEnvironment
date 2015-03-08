__author__ = 'chris'

import Simulator
import World
from matplotlib import animation


FPS = 30 # hardcoded into simulation assumptions

world = World.World(100, 100)
sim = Simulator.Simulator(world, 10, FPS, "images")


# simulator assumes its physics simulation is running at dt = 1/30 s
# would have to recalculate the true animation framerate (to get physically accurate speeds, etc)
# if you change the raw sample rate of the animator function (which accepts arguments in ms)
simlen = 10 # sec
frames = FPS * simlen

def tick(i):
    return sim.tick()

ani = animation.FuncAnimation(sim.fig, tick, frames=frames, blit=True, init_func=sim.setup)

import time

t = time.time()
ani.save('hello.mp4', fps=FPS, extra_args=['-vcodec', 'libx264'])
print "execution time:", time.time() - t
# execution time:  178.861850023

# t = time.time()
# sim.run()
# print "execution time:", time.time() - t
# execution time: 591.768985033

#
# os.chdir("images")
#
# callstring = ["ffmpeg", "-f", "image2", "-i", 'img%08d.png', "-r", str(FPS), "output.mp4"]
#
#
# call(callstring)