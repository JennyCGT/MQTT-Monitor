
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time
from collections import deque
import random

MAX_X = 250   #width of graph
MAX_Y = 70000  #height of graph

# intialize line to horizontal line on 0
line1 = deque([0.0]*MAX_X, maxlen=MAX_X)
line2 = deque([0.0]*MAX_X, maxlen=MAX_X)
line3 = deque([0.0]*MAX_X, maxlen=MAX_X)
line4 = deque([0.0]*MAX_X, maxlen=MAX_X)
line5 = deque([0.0]*MAX_X, maxlen=MAX_X)

plt.close('all')
fig, (ax1,ax2,ax3,ax4) = plt.subplots(4,1)

l1, = ax1.plot([], [])
l2, = ax2.plot([], [])
l3, = ax3.plot([], [])
l4, = ax4.plot([], [])

l=[l1,l2,l3,l4]

for ax in [ax1,ax2,ax3,ax4]:
    ax.set_ylim(-(MAX_Y/2),MAX_Y/2)
    ax.set_xlim(-(MAX_X/2),MAX_X/2)
    ax.grid()

def update(fn, data):
    while True:
        t = time.time()
        #Update Plots
        line1.append(random.randint(10, 20))
        line2.append(random.randint(10, 20))
        line3.append(random.randint(10, 20))
        line4.append(random.randint(10, 20) )

        #Set Data
        l[0].set_data(line1, line1)
        l[1].set_data(line2, line2)
        l[2].set_data(line3, line3)
        l[3].set_data(line4, line4)
        time.sleep(2)

      
ani = anim.FuncAnimation(fig,update,fargs=(0,),frames=1, interval=100)
plt.show()
