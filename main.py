from random import *


class BattleshipBot:
    def __init__(self):
        self.bot_name = "Сука Блять"
        self.student_name = "Matthew Munger"
        self.init()

    def get_move(self, hits, shots):
        """
        :param hits:
        :param shots:
        :return:
        if last shot was sunk ship, random shot
        if last shot was miss, random shot
        if last shot was hit, shoots x + 1, x - 1, y + 1, y - 1
        """
        # TODO: Find boat direction (f | !f)
        # TODO: Shoot in a checkerboard fashion if random shot is required, must wait for 2 to be functional

        last = self.last_shot
        x = last[0]
        y = last[1]
        if last == "init" or hits[x][y] == 2:
            print("Блять")
            # print("last was sunk or init")
            # if type(x) is not str:
                # print("hits[x][y] (%s,%s) = %s" % (x, y, hits[x][y]))
            self.tracking = False
            # print("hits[x][y] == %s" % str(hits[x][y]))
            self.count += 1
            # print(shots)
            # print("Last was sunk or init")
            target = choice(self.coords)
            return self.shoot(target)
        if hits[x][y] == 1:
            print("Сука")
            self.tracking = True
            self.last_hit = [x, y]
            # print("Lol eat my ass i hit u")
            # print("last was hit")
            # last shot hit but didn't sink
            a = x + 1
            b = y
            if self.exists([a, b]):
                # print("exists")
                # print(self.coords)
                # print("hits[a][b] == [%s][%s]" % (a, b))
                if [a, b] in self.coords:
                    # print("hits[a][b] == [%s][%s]" % (a, b))
                    if hits[a][b] == 0:
                        # print("hits[a][b] == [%s][%s]" % (a, b))
                        return self.shoot([a, b])
            a = x - 1
            b = y
            if self.exists([a, b]):
                # print("exists")
                if [a, b] in self.coords:
                    # print("hits[a][b] == [%s][%s]" % (a, b))
                    if hits[a][b] == 0:
                        # print("hits[a][b] == [%s][%s]" % (a, b))
                        return self.shoot([a, b])
            a = x
            b = y + 1
            if self.exists([a, b]):
                # print("exists")
                if [a, b] in self.coords:
                    # print("hits[a][b] == [%s][%s]" % (a, b))
                    if hits[a][b] == 0:
                        # print("hits[a][b] == [%s][%s]" % (a, b))
                        return self.shoot([a, b])
            a = x
            b = y - 1
            if self.exists([a, b]):
                # print("exists")
                if [a, b] in self.coords:
                    # print("hits[a][b] == [%s][%s]" % (a, b))
                    if hits[a][b] == 0:
                        # print("hits[a][b] == [%s][%s]" % (a, b))
                        # print
                        return self.shoot([a, b])
            # print("last shot shit, shooting random...")
            # print("Shooting random?")
            return self.shoot(choice(self.coords))
        else:
            # print("last was miss")
            if self.tracking:
                # print("tracking...")
                x = self.last_hit[0]
                y = self.last_hit[1]
                a = x + 1
                b = y
                if self.exists([a, b]):
                    if hits[a][b] == 0 and [a, b] in self.coords:
                        return self.shoot([a, b])
                a = x - 1
                b = y
                if self.exists([a, b]):
                    if hits[a][b] == 0 and [a, b] in self.coords:
                        return self.shoot([a, b])
                a = x
                b = y + 1
                if self.exists([a, b]):
                    if hits[a][b] == 0 and [a, b] in self.coords:
                        return self.shoot([a, b])
                a = x
                b = y - 1
                if self.exists([a, b]):
                    if hits[a][b] == 0 and [a, b] in self.coords:
                        return self.shoot([a, b])
                # print("last shot shit, shooting random...")
                # print("tracking failed, resulting to random")
                target = choice(self.coords)
            else:
                # print("random shot...")
                target = choice(self.coords)
            return self.shoot(target)

    def shoot(self, target):
        self.coords.remove(target)
        self.last_shot = target
        return target

    def exists(self, target):
        return target in self.board

    def get_setup(self):
        """
        Fully random ship placements, without overlaps, within the board.
        """
        self.init()
        # TODO: Add gay var
        ls = [2, 5, 4, 3, 3]
        ships = []
        occs = []
        for l in ls:
            a = self.new_ship(l, ships, occs)
            ships.append((l, a[0], a[1], a[2]))
            occs = a[3]
        return ships

    def new_ship(self, ship, ships, occs):
        l = ship
        f = randint(0, 1)
        max = 9 - l + 1
        temp_occs = []
        # TODO: Optimise f to have only one tree that separates later.
        if l == 2:  # Add boat in last coord cuz yeah ppl be gay
            temp_occs = [[9, 8], [9, 9]]
            return 9, 8, 1, temp_occs
        if not f:
            x = randint(0, max)
            y = randint(0, 9)
            for a in range(x, x + l):
                temp_occs.append([a, y])
            for temp_occ in temp_occs:
                if temp_occ in occs:
                    return self.new_ship(ship, ships, occs)
            for temp_occ in temp_occs:
                occs.append(temp_occ)
            return x, y, f, occs
        else:
            x = randint(0, 9)
            y = randint(0, max)
            for b in range(y, y + l):
                temp_occs.append([x, b])
            for temp_occ in temp_occs:
                if temp_occ in occs:
                    return self.new_ship(ship, ships, occs)
            for temp_occ in temp_occs:
                occs.append(temp_occ)
            return x, y, f, occs

    @staticmethod
    def check_ship_layout_validity(ships):
        """
        Checks position of each ship in ships[] for overlaps and grid border crossing.
        """
        occs = []
        ls = [5, 4, 3, 3, 2]
        count = 0
        for ship in ships:
            l = ship[0]
            if ship[3] == 0:
                for x in range(ship[1], ship[1] + l):
                    coord = [x, ship[2]]
                    if coord in occs:
                        return 0
                    occs.append(coord)
            else:
                for y in range(ship[2], ship[2] + l):
                    coord = [ship[1], y]
                    if coord in occs:
                        return 0
                    occs.append(coord)
            count += 1
        return 1

    def success_checker(self):
        """
        Check success rate of get_setup().
        """
        yes = 0
        no = 0
        for i in range(0, 1000):
            s = BattleshipBot().get_setup()
            if self.check_ship_layout_validity(s):
                yes += 1
            else:
                no += 1
        print("Works: {0}, Fails: {1}, Works %: {2}".format(yes, no, yes / (yes + no) * 100))

    def init(self):
        self.last_shot = "init"
        self.coords = []
        for a in range(0, 10):
            for b in range(0, 10):
                self.coords.append([a, b])
        self.board = self.coords
        self.count = 0
        self.tracking = False
        self.last_hit = None

# ships = BattleshipBot().get_setup()
# print("ships = %s" % ships)

# BattleshipBot().success_checker()
