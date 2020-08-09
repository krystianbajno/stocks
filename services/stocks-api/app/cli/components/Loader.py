class Loader:
    def __init__(self):
        self.__anim = self.__add
        self.__patterns = ["-", "/", "|", "\\"]
        self.__st = 0

    def __add(self):
        self.__st = self.__st + 1

    def __subtract(self):
        self.__st = 0

    def step(self):
        if self.__st >= len(self.__patterns) - 1:
            self.__anim = self.__subtract
        elif self.__st == 0:
            self.__anim = self.__add

        self.__anim()

    def print(self):
        return self.__patterns[self.__st]
