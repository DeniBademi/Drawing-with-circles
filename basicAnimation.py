# Code by Denis Zahariev(DeniBademi) 2021
# Made with <3 and python
# Email: denis.zaharievv@gmail.com

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import math
from scipy.integrate import quad
delay = 10


class drawingMachine:
    trail_length = 300
    
    def __init__(self, c):
        self.c=c
        self.x_data = []
        self.y_data = []

    def build(self, tl,n):
        self.scenario = []
        
        self.trail_length = int(tl/1.1)
        for t in range(tl):
            self.scenario.append([]) # frame
            self.scenario[t-1].append([]) # dimension
            self.scenario[t-1].append([])

            z = 0 + 0*1j

            for i in sum(zip(range(n+1, 2*n+1), range(n-1, -1, -1)), (n,)):
                old_z = z
                z += np.exp(2*np.pi*1j*(i-n)*t/tl)*self.c[i] 

                self.scenario[t-1][0].append(z.real)
                self.scenario[t-1][1].append(z.imag)



def animateF(drawingMachine,tl):
    global ani
    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-6, 6), ylim=(-6, 6))
    history, = ax.plot([1], [1], 'r-', lw=1)


    ax.set_aspect('equal')
    ax.grid()

    axtext = fig.add_axes([0.0,0.95,0.3,0.05])
    axtext.axis("off")
    time = axtext.text(0.5,0.5, str(0), ha="left", va="top")
    line, = ax.plot([], [], '-', lw=1)


    def animation_frame(i):
        thisx = drawingMachine.scenario[i][0]
        thisy = drawingMachine.scenario[i][1]

        drawingMachine.x_data.extend([thisx[-1],thisx[-1]])
        drawingMachine.y_data.extend([thisy[-1],thisy[-1]])

        line.set_data(thisx, thisy)
        time.set_text("time = " + str(i*delay / 1000))
        history.set_data(drawingMachine.x_data[-drawingMachine.trail_length*2:],drawingMachine.y_data[-drawingMachine.trail_length*2:])

        return line, time, history,

    ani = animation.FuncAnimation(fig, animation_frame, np.arange(1, tl-1),
    interval=delay, blit=True )

    plt.show()



