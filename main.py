from random import *


class BattleshipBot:
    def __init__(self):
        self.bot_name = "I do have a dad vIRGIN"
        self.student_name = "Matthew Munger"
        self.last_shot = "init"
        self.coords = []
        for a in range(0, 10):
            for b in range(0, 10):
                self.coords.append([a, b])

    def get_move(self, hits, shots):
        """
        :param hits:
        :param misses:
        :return:
        if last shot was sunk ship, random shot
        if last shot was miss, random shot
        if last shot was hit, shoots x + 1, x - 1, y + 1, y - 1
        """
        last = self.last_shot
        x = last[0]
        y = last[1]
        if last == "init" or hits[x][y] == 2:
            target = choice(self.coords)
            return self.shoot(target)
        if hits[x][y] == 1:
            # last shot hit but didn't sink
            if hits[x + 1] [y] == 0 and hits[x + 1][y] in self.coords:
                return self.shoot([x + 1, y])
            if hits[x - 1] [y] == 0 and hits[x - 1][y] in self.coords:
                return self.shoot([x - 1, y])
            if hits[x] [y + 1] == 0 and hits[x][y + 1] in self.coords:
                return self.shoot([x, y + 1])
            if hits[x] [y - 1] == 0 and hits[x][y - 1] in self.coords:
                return self.shoot([x, y - 1])

    def shoot(self, target):
        self.coords.remove(target)
        self.last_shot = target
        return target

    def get_setup(self):
        """
        Fully random ship placements, without overlaps or boarder crossings.
        """
        ls = [5, 4, 3, 3, 2]
        ships = []
        temp_ships = []
        occs = []
        for temp_ship in ls:
            l = temp_ship
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


ships = BattleshipBot().get_setup()
print("ships = %s" % ships)

BattleshipBot().success_checker()