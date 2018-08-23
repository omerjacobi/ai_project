import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self):
        self.barNum = 1
        self.pieNum = 1

    def bar(self, vals, names, x_lable, y_lable, title, save=True, show=True):
        ind = np.arange(len(vals))
        plt.bar(ind, vals,0.35)
        plt.ylabel(y_lable)
        plt.title(title)

        plt.xticks(ind, names)
        plt.yticks(np.arange(0, max(vals)*1.1, np.round(max(vals)/10)))
        if save:
            plt.savefig(title + str(self.barNum) + ".png")
            self.barNum += 1
        if show:
            plt.show()
        plt.close()

    def pie(self, x, y, x_lable, y_lable, title, save=True, show=True):
        plt.xlabel(x_lable)
        plt.ylabel(y_lable)
        plt.title(title)
        plt.pie(x, y)
        if save:
            plt.savefig(title + str(self.pieNum) + ".png")
            self.pieNum += 1
        if show:
            plt.show()
        plt.close()

    def line(self, x, y, x_lable, y_lable, title, save=True, show=True):

        plt.xlabel(x_lable)
        plt.ylabel(y_lable)
        plt.title(title)
        plt.plot(x, y,0.35)
        if save:
            plt.savefig(title + str(self.pieNum) + ".png")
            self.pieNum += 1
        if show:
            plt.show()


# heuristics_str= ['original', 'fn_lost_marbles', 'sumito', 'defensive', 'aggressive']
# heuristics_str2 = [13243432422,3,4,4,4]
#
# pl = Plotter()
# pl.bar(heuristics_str2, heuristics_str, 'td', 'sd', 'title')
# pl.bar(heuristics_str2, heuristics_str, 'tasd', 'ssad', 'title')
