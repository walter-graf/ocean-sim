#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

# constants

max_rows = 25
max_cols = 70
default_num_obstacles = 75
default_num_predators = 20
default_num_prey = 150
default_num_iterations = 1000
max_num_iterations = 1000
water_image = '-'
prey_image = 'f'
pred_image = 'S'
obstacle_image = '#'
time_to_feed = 6
time_to_reproduce = 6

# random.random() = randReal()
# random.randint(a,b) = nextIntBetween(a,b)

#for better clarity consider using row/col terminology throughout the code
class Coordinate:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,x):
        self.x = x
    def set_y(self,y):
        self.y = y
    def assign(self,other):
        self.x = other.x
        self.y = other.y
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y
    def __ne__(self,other):
        return self.x != other.x or self.y != other.y

class Cell:
    def __init__(self,coord, ocean):
        self.offset = coord
        self.image = water_image
        # crucial design element: every cell is linked to 'the' ocean
        self.ocean = ocean

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset

    def get_image(self):
        return self.image

    def display(self):
        print(self.image, end='')

    def process(self):
        pass

    # private section

# called by move_from (but not needed)
    def get_cell_at(self, coord):
        return self.ocean.water[coord.get_y()][coord.get_x()]

    def assign_cell_at(self,coord,cell):
        # called multiple times with different parameters by move_from
        self.ocean.water[coord.get_y()][coord.get_x()] = cell

    def get_neighbor_with_image(self,image):
        # identify all neighbors with the wanted image
        # randomly return one of them
        # if no neighbor exists return current cell
        count = 0
        neighbors = [None, None, None, None]
        if self.north().get_image() == image:
            neighbors[count] = self.north()
            count +=1
        if self.south().get_image() == image:
            neighbors[count] = self.south()
            count +=1
        if self.east().get_image() == image:
            neighbors[count] = self.east()
            count +=1
        if self.west().get_image() == image:
            neighbors[count] = self.west()
            count +=1
        if count == 0:
            return self
        else:
            return neighbors[random.randint(0, count-1)]
        
    def get_empty_neighbor_coord(self):
        return self.get_neighbor_with_image(water_image).get_offset()

# Verwendung von prey_image eventuell problematisch
    def get_prey_neighbor_coord(self):
        return self.get_neighbor_with_image(prey_image).get_offset()

    def north(self):
        if self.offset.get_y() > 0:
            y = self.offset.get_y() - 1
        else:
            # wrap around
            y = self.ocean.num_rows - 1
        return self.ocean.water[y][self.offset.get_x()]
        
    def south(self):
        # modulo num_rows results in wrap around for num_rows
        y = (self.offset.get_y() + 1) % self.ocean.num_rows
        return self.ocean.water[y][self.offset.get_x()]

    def east(self):
        x = (self.offset.get_x() + 1) % self.ocean.num_cols
        return self.ocean.water[self.offset.get_y()][x]

    def west(self):
        if self.offset.get_x() > 0:
            x = self.offset.get_x() - 1
        else:
            x = self.ocean.num_cols - 1
        return self.ocean.water[self.offset.get_y()][x]

# double check
    def reproduce(self, coord):
        return Cell(coord, self.ocean)

class Prey(Cell):
    def __init__(self, coord, ocean):
        Cell.__init__(self, coord, ocean)
        self.time_to_reproduce = time_to_reproduce
        self.image = prey_image

    def process(self):
        self.move_from(self.offset, self.get_empty_neighbor_coord())

    # private section
# double check
# should f (from) not always be self.offset?
    def move_from(self,f,t):
        # move current cell to new location 't'
        # if time to reproduce is up leave a child at the from 'f' location
        # otherwise leave an empty cell at the from 'f' location
        self.time_to_reproduce -= 1
        if t != f:
            self.set_offset(t)
            self.assign_cell_at(t, self)
            if self.time_to_reproduce <= 0:
                self.time_to_reproduce = time_to_reproduce
                self.assign_cell_at(f, self.reproduce(f))
            else:
                self.assign_cell_at(f, Cell(f, self.ocean))

    def reproduce(self, coord):
    #    self.ocean.num_prey += 1
       self.ocean.set_num_prey(self.ocean.get_num_prey() + 1)
       return Prey(coord, self.ocean)


class Predator(Prey):
    def __init__(self, coord, ocean):
        Prey.__init__(self, coord, ocean)
        self.time_to_feed = time_to_feed
        self.image = pred_image

    def process(self):
        self.time_to_feed -= 1
        if self.time_to_feed <= 0:
            # predator dies
            self.assign_cell_at(self.offset, Cell(self.offset, self.ocean))
            # self.ocean.num_predators -= 1
            self.ocean.set_num_predators(self.ocean.get_num_predators() - 1)
        else:
            # look for prey
            to = self.get_prey_neighbor_coord()
            if to != self.offset:
                # prey found
                # move to prey and eat it / reproduce if time has come
                self.move_from(self.offset, to)
                # self.ocean.num_prey -= 1
                self.ocean.set_num_prey(self.ocean.get_num_prey() - 1)
                self.time_to_feed = time_to_feed
            else:
                # no prey found
                # try to find an empty cell instead / reproduce if time has come
                self.move_from(self.offset, self.get_empty_neighbor_coord())

    # private section
    def reproduce(self, coord):
        self.ocean.set_num_predators(self.ocean.get_num_predators() + 1)
        return Predator(coord, self.ocean)

class Obstacle(Cell):
    def __init__(self, coord, ocean):
        Cell.__init__(self, coord, ocean)
        self.image = obstacle_image

class Ocean:
    def __init__(self):
        self.num_rows = max_rows
        self.num_cols = max_cols
        self.size = self.num_rows * self.num_cols

        self.num_obstacles = default_num_obstacles
        self.num_predators = default_num_predators
        self.num_prey = default_num_prey

        self.water = [[ None for col in range(max_cols)] for row in range(max_rows)]

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.water[row][col] = Cell(Coordinate(col,row), self)
        
        # self.num_obstacles = int(input('\n\nEnter number of obstacles (default = 75): '))
        self.num_obstacles = self.read_int('\nEnter number of obstacles (default = %d): ', default_num_obstacles)
        if(self.num_obstacles > self.size):
            self.num_obstacles = self.size
        print('Number of obstacles accepted = ', self.num_obstacles)
        
        # self.num_predators = int(input('\n\nEnter number of predators (default = 20): '))
        self.num_predators = self.read_int('\nEnter number of predators (default = %d): ', default_num_predators)
        if(self.num_predators > self.size - self.num_obstacles):
            self.num_predators = self.size - self.num_obstacles
        print('Number of predators accepted = ', self.num_predators)

        # self.num_prey = int(input('\n\nEnter number of prey (default = 150): '))
        self.num_prey = self.read_int('\n\nEnter number of prey (default = %d): ', default_num_prey)
        if(self.num_prey > self.size - self.num_obstacles - self.num_predators):
            self.num_prey = self.size - self.num_obstacles - self.num_predators
        print('Number of prey accepted = ', self.num_prey)

        self.add_obstacles()
        self.add_predators()
        self.add_prey()
        self.display_stats(-1)
        self.display_cells()
        self.display_border()
    
    def get_num_prey(self):
        return self.num_prey

    def get_num_predators(self):
        return self.num_predators

    def set_num_prey(self, num):
        self.num_prey = num

    def set_num_predators(self, num):
        self.num_predators = num
    
    def read_int(self, text, default):
        s = input(text % default)
        if len(s) == 0:
            i = default
        else:
            i = int(s)
        return i

    def run(self):
        # num_iterations = default_num_iterations
        num_iterations = self.read_int('\nEnter number of iterations (default and max = %d): ', default_num_iterations)
        # num_iterations = int(input('\nEnter number of iterations (default max = 1000): '))
        if num_iterations > max_num_iterations:
            num_iterations = max_num_iterations
        print('Number of iterations accepted = %d\nbegin run...\n' % num_iterations)
        for iteration in range(num_iterations):
            if self.num_predators > 0 and self.num_prey > 0:
                for row in range(self.num_rows):
                    for col in range(self.num_cols):
                        self.water[row][col].process()
                self.display_stats(iteration)
                self.display_cells()
                self.display_border()
        print('\nEnd of Simulation\n')

    # private section

    def add_obstacles(self):
        for n in range(self.num_obstacles):
            coord = self.get_empty_cell_coord()
            self.water[coord.get_y()][coord.get_x()] = Obstacle(coord, self)

    def add_predators(self):
        for n in range(self.num_predators):
            coord = self.get_empty_cell_coord()
            self.water[coord.get_y()][coord.get_x()] = Predator(coord, self)
            
    def add_prey(self):
        for n in range(self.num_prey):
            coord = self.get_empty_cell_coord()
            self.water[coord.get_y()][coord.get_x()] = Prey(coord, self)

    def get_empty_cell_coord(self):
        while True:
            x = random.randint(0, self.num_cols-1)
            y = random.randint(0, self.num_rows-1)
            if self.water[y][x].get_image() == water_image:
                break
        return self.water[y][x].get_offset()

    def display_border(self):
        print(self.num_cols*'*')

    def display_cells(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.water[row][col].display()
            print()

    def display_stats(self, iteration):
        iteration+=1
        print('\nIteration number: %d Obstacles: %d Predators: %d Prey: %d' % (iteration, self.num_obstacles, self.num_predators, self.num_prey))
        self.display_border()


# main program

ocean = Ocean()
ocean.run()