import matplotlib.pyplot as plt
import matplotlib.animation as anim
from math import sqrt, pi
import random
import serial

batch = 1
interactive = 1

PORT = "COM16"  # change this to the port number microbit is on
# on Windows:
# Control Panel -> Devices and Printers -> Under Devices and Printers look for DEVICE MANAGER
# Once Device Manager is open: Ports(COM & LPT) -> look for mBed Serial Port (COM 16)
if interactive:
    ser = serial.Serial(port=PORT, baudrate=115200)

members = {"red": [], "blue": [], "green": [], "yellow": [],
           "orange": [], "cyan": [], "magenta": [], "black": []}


def in_circle(x, y):
    return sqrt(x**2 + y**2) < 1


def print_stats():
    """
    A function to return the current overall guess
    :return: two-long list [pi_guess, number_of_drops]
    """
    num_in = 0
    num_drops = 0
    for m in members.keys():
        xx = [members[m][ii][0] for ii in range(len(members[m]))]
        yy = [members[m][ii][1] for ii in range(len(members[m]))]
        num_drops += len(members[m])
        for xi, yi in zip(xx, yy):
            if in_circle(xi, yi):
                num_in += 1
    return [4.0*(float(num_in)/max(1, num_drops)), num_drops]


def plot_cont(fun, xmax):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    fig.subplots_adjust(bottom=0.25, top=0.95)
    circle1 = plt.Circle((0.5, 0.5), 0.5, color='r', fill=False)

    def update():
        color, a, b = fun()
        members[color].append((a, b))

        ax.clear()
        plt.xlim(0, 1)
        plt.ylim(0, 1)

        for m in members.keys():
            xx = [members[m][ii][0] for ii in range(len(members[m]))]
            yy = [members[m][ii][1] for ii in range(len(members[m]))]

            num_in = 0
            num_drops = len(members[m])
            for xi, yi in zip(xx, yy):
                if in_circle(xi, yi):
                    num_in += 1
            mypi = 4.0 * (float(num_in) / max(1, num_drops))
            label = "Guessed %s times, pi = %2.3f, Error: %2.1f percent." % (
                num_drops, mypi, abs(100 - 100 * float(mypi / pi)))
            ax.scatter(xx, yy, color=m, s=50, label=label)

        plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)

        ax.add_artist(circle1)
        piguess, drops = print_stats()
        total_guess = (r'$\pi = %f\ guessed\ %d\ times, error %s\ percent.$'
                       % (piguess, drops, abs(100-100*float(piguess/pi))))
        txt = plt.text(0.27, 1.025, total_guess)
        ax.add_artist(txt)

    anim.FuncAnimation(fig, update, frames=xmax, repeat=False, interval=1)
    plt.show()


def drop():
    """
    Get the next guess. If interactive use serial, else make a random guess
    :return:
    """
    if interactive:
        v = str(ser.readline(500))
        p = v.split("_")
        color = p[1]
        r1 = p[2]
        r2 = p[3].replace("\'", "")
        return color, float(r1) / 1000, float(r2) / 1000
    else:
        c = members.keys()[int(random.random()*8)]  # randomly pick a color
        return c, random.random(), random.random()


plot_cont(drop, 100000)
