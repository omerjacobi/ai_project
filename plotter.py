import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        self.barNum = 1
        self.pieNum = 1

    def bar(self, x, y, x_lable, y_lable, title, show=True):
        plt.xlabel(x_lable)
        plt.ylabel(y_lable)
        plt.title(title)
        plt.bar(x, y)
        plt.savefig(title + str(self.barNum) + ".png")
        self.barNum += 1
        if show:
            plt.show()

    def pie(self, x, y, x_lable, y_lable, title, show=True):
        plt.xlabel(x_lable)
        plt.ylabel(y_lable)
        plt.title(title)
        plt.pie(x, y)
        plt.savefig(title + str(self.pieNum) + ".png")
        self.pieNum += 1
        if show:
            plt.show()
