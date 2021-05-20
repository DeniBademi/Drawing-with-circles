# Code by Denis Zahariev(DeniBademi) 2021
# Made with <3 and python
# Email: denis.zaharievv@gmail.com

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.cm import get_cmap
from basicAnimation import drawingMachine as dW
from basicAnimation import animateF
import math
import scipy as sp
from math import sqrt
#mouse_xy= np.array([[]],dtype=complex)
mouse_xy= []


def plot_fourier2(k):
    dx = 0.006
    L = 6

    mouse_x, mouse_y = ([item[0] for item in mouse_xy],[item[1] for item in mouse_xy])

    x = np.linspace(-L+dx, L-dx, len(mouse_x))
    fig, ax = plt.subplots()
    ax.set_xlim([-L,L])
    ax.set_ylim([-L, L])


    
    # Calculate Fourier Coefficients
    name = "Accent"
    cmap = get_cmap('tab10')
    colors = cmap.colors
    ax.set_prop_cycle(color = colors)

    A0x = np.sum(mouse_x * np.ones_like(x)) * dx # average # multiples the elements in the two arrays with each one
    A0y = np.sum(mouse_y * np.ones_like(x)) * dx

    mousex = mouse_x - A0x
    mousey = mouse_y - A0y

    A0x = np.sum(mousex * np.ones_like(x)) * dx # average # multiples the elements in the two arrays with each one
    A0y = np.sum(mousey * np.ones_like(x)) * dx
    #501 so we need to normalize

    plot_x = A0x/2
    plot_y = A0y/2

    A = np.zeros(k)
    B = np.zeros(k)

    Ay = np.zeros(k)
    By = np.zeros(k)



    for k in range(k):
        A[k] = np.sum(mouse_x * np.cos(np.pi*(k+1)*x/L)) * dx
        B[k] = np.sum(mouse_x * np.sin(np.pi*(k+1)*x/L)) * dx
        plot_x += A[k] * np.cos((k+1) * np.pi*x/L) + B[k]*np.sin((k+1)*np.pi*x/L)

        Ay[k] = np.sum(mouse_y * np.cos(np.pi*(k+1)*x/L)) * dx
        By[k] = np.sum(mouse_y * np.sin(np.pi*(k+1)*x/L)) * dx
        plot_y += Ay[k] * np.cos((k+1) * np.pi*x/L) + By[k]*np.sin((k+1)*np.pi*x/L)
        
    ax.plot(plot_x/L,plot_y/L,'-')
    

    
    plt.show()

def plot_fourier(n):
    global mouse_xy
    L = 6
    print(mouse_xy)
    tl = len(mouse_xy)
    c = []
    for i in range(n, -n-1, -1):
        c.append(sum(np.exp(2*np.pi*1j*i*t/tl)*(mouse_xy[t][0]+mouse_xy[t][1]*1j) for t in range(tl))/tl)
    

   # print(c)
    #print(tl)
    drawingMachine = dW(c)
    drawingMachine.build(tl,n)
    animateF(drawingMachine,tl)      
        
class MouseController:
    lock = None  # only one can be animated at a time

    def __init__(self, rect):
        self.rect = rect
        self.press = None

    def connect(self):
        """Connect to all the events we need."""
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        """Handles button_press_event and locks the animation"""

        if (MouseController.lock is not None):
            return

        MouseController.lock = self


    def on_motion(self, event):
        """Store mouse movement data in the array if button is pressed."""
        if (MouseController.lock is not self):
            return

        mouse_xy.append([event.xdata,event.ydata])
        history.set_data([item[0] for item in mouse_xy],[item[1] for item in mouse_xy])
        

    def on_release(self, event):
        """Unlocks the animation and stops the data logging."""
        if MouseController.lock is not self:
            return

        self.press = None
        MouseController.lock = None

        plot_fourier(80)

    def disconnect(self):
        """Disconnect all callbacks."""

        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)



fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-6, 6), ylim=(-6, 6))
history, = ax.plot([], [], '-', lw=1)


mouse = MouseController(history)

mouse.connect()


def animate(i):
    history.set_data([item[0] for item in mouse_xy],[item[1] for item in mouse_xy])
    return history, 

ani = animation.FuncAnimation(fig, animate,
                              interval=25, blit=True)
                  
plt.show()