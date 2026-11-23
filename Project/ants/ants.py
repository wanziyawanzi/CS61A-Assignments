"""CS 61A presents Ants Vs. SomeBees."""

import random
from ucb import main, interact, trace
from collections import OrderedDict

################
# Core Classes #
################


class Place:
    """A Place holds insects and has an exit to another Place.
    一个 Place 对象中存放昆虫，并且有一个通向另一个 Place 的出口"""
    is_hive = False

    def __init__(self, name, exit=None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit为出口添加一个入口。
        # BEGIN Problem 2
        "*** YOUR CODE HERE ***"
        if self.exit is not None:
            self.exit.entrance = self
        # END Problem 2

    def add_insect(self, insect):
        """Asks the insect to add itself to this place. This method exists so
        that it can be overridden in subclasses.
        **请求昆虫将自身添加到此 Place 中。提供此方法是为了让子类能够重写它。**"""
        insect.add_to(self)

    def remove_insect(self, insect):
        """Asks the insect to remove itself from this place. This method exists so
        that it can be overridden in subclasses.
        **请求昆虫将自身从此 Place 中移除。提供此方法是为了让子类能够重写它。**"""
        insect.remove_from(self)

    def __str__(self):
        return self.name


class Insect:
    """An Insect, the base class of Ant and Bee, has health and a Place.
    **Insect 是 Ant 和 Bee 的基类，具有 health（生命值）和一个 Place（地点）。**"""

    next_id = 0  # Every insect gets a unique id number
    damage = 0
    # ADD CLASS ATTRIBUTES HERE
    is_waterproof = False

    def __init__(self, health, place=None):
        """Create an Insect with a health amount and a starting PLACE.
        **创建一个带有 health（生命值）数值和起始 PLACE（地点）的 Insect（昆虫）。**"""
        self.health = health
        self.place = place

        # assign a unique ID to every insect
        self.id = Insect.next_id
        Insect.next_id += 1

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the insect from its place if it
        has no health remaining.
        **将 health（生命值）减少 AMOUNT；
        如果昆虫没有剩余生命值，则将其从其所在的 Place（地点）中移除。**
        
        >>> test_insect = Insect(5)
        >>> test_insect.reduce_health(2)
        >>> test_insect.health
        3
        """
        self.health -= amount
        if self.health <= 0:
            self.zero_health_callback()
            self.place.remove_insect(self)

    def action(self, gamestate):
        """The action performed each turn.**每回合执行的动作。**"""

    def zero_health_callback(self):
        """Called when health reaches 0 or below.**当生命值降到 0 或以下时被调用。**"""

    def add_to(self, place):
        self.place = place

    def remove_from(self, place):
        self.place = None

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.health, self.place)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony.
    **Ant（蚂蚁）占据一个 Place（地点），并为蚁群工作。**"""

    implemented = False  # **只应实例化已经实现的 Ant 类。**Only implemented Ant classes should be instantiated
    food_cost = 0
    is_container = False
    # ADD CLASS ATTRIBUTES HERE
    fanbei = False
    
    def __init__(self, health=1):
        super().__init__(health)

    def can_contain(self, other):
        return False

    def store_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def remove_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def add_to(self, place):
        if place.ant is None:
            place.ant = self
        # BEGIN Problem 8b
        elif place.ant.can_contain(self):
            place.ant.ant_contained = self
        elif self.can_contain(place.ant):
            self.ant_contained = place.ant
            place.ant = self
        else:
            assert place.ant is None, 'Too many ants in {0}'.format(place)
            # END Problem 8b
        Insect.add_to(self, place)

    def remove_from(self, place):
        if place.ant is self:
            place.ant = None
        elif place.ant is None:
            assert False, '{0} is not in {1}'.format(self, place)
        else:
            place.ant.remove_ant(self)
        Insect.remove_from(self, place)

    def double(self):
        """Double this ants's damage, if it has not already been doubled.
        **如果这只蚂蚁的伤害尚未翻倍，则将其伤害翻倍。**"""
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        if not self.fanbei:
            self.damage *= 2
            self.fanbei = True
        # END Problem 12


class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony.
    **HarvesterAnt（采集蚁）每回合为蚁群额外生产 1 单位食物。**"""

    name = 'Harvester'
    implemented = True
    # OVERRIDE CLASS ATTRIBUTES HERE
    food_cost = 2

    def action(self, gamestate):
        """Produce 1 additional food for the colony.
            为蚁群额外生产 1 单位食物
        gamestate -- The GameState, used to access game state information.
        """
        # BEGIN Problem 1
        "*** YOUR CODE HERE ***"
        gamestate.food += 1
        # END Problem 1


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range.
    **ThrowerAnt（投掷蚁）每回合向其范围内最近的 Bee（蜜蜂）投掷一片叶子。**"""

    name = 'Thrower'
    implemented = True
    damage = 1
    # ADD/OVERRIDE CLASS ATTRIBUTES HERE
    food_cost = 3
    lower_bound = 0
    upper_bound = float('inf')  #上界默认为无穷大

    def nearest_bee(self):
        """Return the nearest Bee in a Place (that is not the hive) connected to
        the ThrowerAnt's Place by following entrances.
        **返回通过沿入口（entrances）连接到 ThrowerAnt 所在地点的 Place 中
        （且该 Place 不是蜂巢）距离最近的 Bee。**

        **如果没有这样的 Bee（或者范围内没有 Bee），此方法返回 None。**
        This method returns None if there is no such Bee (or none in range).
        """
        # BEGIN Problem 3 and 4
        cnt = self.lower_bound
        cur_place = self.place
        for _ in range(self.lower_bound):     #确定下限对应的cur地点
            if cur_place.is_hive:
                return None
            cur_place = cur_place.entrance
        # 在 upper_bound 范围内寻找蜜蜂  
        while not cur_place.is_hive and cnt <= self.upper_bound:
            cnt += 1
            if cur_place.bees:
                return random_bee(cur_place.bees) 
            else:
                cur_place = cur_place.entrance
        return None
        # END Problem 3 and 4

    def throw_at(self, target):
        """Throw a leaf at the target Bee, reducing its health.
        **向目标 Bee 投掷一片叶子，降低其生命值。**"""
        if target is not None:
            target.reduce_health(self.damage)

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range.
        **向范围内最近的 Bee（蜜蜂）投掷一片叶子。**"""
        self.throw_at(self.nearest_bee())


def random_bee(bees):
    """Return a random bee from a list of bees, or return None if bees is empty.
    **从蜜蜂列表中随机返回一只蜜蜂；如果列表为空，则返回 None。**"""
    assert isinstance(bees, list), \
        "random_bee's argument should be a list but was a %s" % type(bees).__name__
    if bees:
        return random.choice(bees)

##############
# Extensions #
##############


class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away.
    **一种 ThrowerAnt（投掷蚁），只向距离最多相隔 3 个 Place（地点）的 Bee（蜜蜂）投掷叶子。**"""

    name = 'Short'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI
    upper_bound = 3
    # END Problem 4


class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away.
    **一种 ThrowerAnt（投掷蚁），只向距离至少相隔 5 个 Place（地点）的 Bee（蜜蜂）投掷叶子。**"""

    name = 'Long'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI
    lower_bound = 5
    # END Problem 4


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires.
    **FireAnt（火蚁）在死亡时烤焦其所在 Place（地点）中的任何 Bee（蜜蜂）。**"""

    name = 'Fire'
    damage = 3
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 5
    implemented = True   # Change to True to view in the GUI
    # END Problem 5

    def __init__(self, health=3):
        """Create an Ant with a HEALTH quantity."""
        super().__init__(health)

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the FireAnt from its place if it
        has no health remaining.
        将生命值减少 AMOUNT；如果 FireAnt（火蚁）没有剩余生命值，则将其从所在 Place（地点）中移除。

        确保减少当前 Place 中每只 Bee（蜜蜂）的生命值，并且如果 FireAnt 死亡，则施加额外伤害。
        Make sure to reduce the health of each bee in the current place, and apply
        the additional damage if the fire ant dies.
        """
        # BEGIN Problem 5
        "*** YOUR CODE HERE ***"
        for bee in self.place.bees[:]:
            if self.health-amount > 0:
                bee.reduce_health(amount)
            else:
                bee.reduce_health(amount+self.damage)
        super().reduce_health(amount)
        # END Problem 5

# BEGIN Problem 6
# The WallAnt class
class WallAnt(Ant):
    name = 'Wall'
    food_cost = 4
    implemented = True
    def __init__(self, health=4):
        super().__init__(health)
# END Problem 6

# BEGIN Problem 7
# The HungryAnt Class
class HungryAnt(Ant):
    name = 'Hungry'   
    food_cost = 4   
    chew_cooldown = 3   #咀嚼所需的回合数
    implemented = True
    def __init__(self, health=1):
        super().__init__(health)
        self.cooldown = 0   #其剩余咀嚼回合数
        
    def action(self,gamestate):
        if self.cooldown != 0:
            self.cooldown -= 1
        elif self.place.bees:
            bee = random_bee(self.place.bees)
            bee.reduce_health(bee.health)
            self.cooldown = HungryAnt.chew_cooldown
    
# END Problem 7


class ContainerAnt(Ant):
    """
    ContainerAnt can share a space with other ants by containing them.
    **ContainerAnt（容器蚁）可以通过容纳其他蚂蚁来与它们共享同一空间。**
    """
    is_container = True

    def __init__(self, health):
        super().__init__(health)
        self.ant_contained = None

    def can_contain(self, other):
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        return False if self.ant_contained or other.is_container else True 
        # END Problem 8a

    def store_ant(self, ant):
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        self.ant_contained = ant
        # END Problem 8a

    def remove_ant(self, ant):
        if self.ant_contained is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.ant_contained = None

    def remove_from(self, place):
        # Special handling for container ants**对 ContainerAnt（容器蚁）的特殊处理。**
        if place.ant is self:
            # Container was removed. Contained ant should remain in the game
            #**容器蚁已被移除。被容纳的蚂蚁应仍然保留在游戏中。**
            place.ant = place.ant.ant_contained
            Insect.remove_from(self, place)
        else:
            # default to normal behavior
            Ant.remove_from(self, place)

    def action(self, gamestate):
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        if self.ant_contained:
            self.ant_contained.action(gamestate)
        # END Problem 8a          


class BodyguardAnt(ContainerAnt):
    """BodyguardAnt provides protection to other Ants.
    **BodyguardAnt（保镖蚁）为其他 Ant（蚂蚁）提供保护。**"""

    name = 'Bodyguard'
    food_cost = 4
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 8c
    implemented = True   # Change to True to view in the GUI
    def __init__(self, health=2):
        super().__init__(health)
    # END Problem 8c

# BEGIN Problem 9
# The TankAnt class
class TankAnt(ContainerAnt):
    name = 'Tank'
    food_cost = 6
    damage = 1
    implemented = True
    
    def __init__(self, health=2):
        super().__init__(health)
        
    def action(self,gamestate):
        super().action(gamestate)
        if self.place.bees:
            for bee in self.place.bees[:]:
                bee.reduce_health(self.damage)
# END Problem 9


class Water(Place):
    """Water is a place that can only hold waterproof insects.
    **Water（水域）是一个只能容纳防水昆虫的 Place（地点）。**"""

    def add_insect(self, insect):
        """Add an Insect to this place. If the insect is not waterproof, reduce
        its health to 0.**将一只 Insect（昆虫）添加到此 Place（地点）。
        如果该昆虫不防水，则将其生命值降为 0。**"""
        # BEGIN Problem 10
        "*** YOUR CODE HERE ***"
        super().add_insect(insect)
        if not insect.is_waterproof:
            insect.reduce_health(insect.health)
        # END Problem 10

# BEGIN Problem 11
# The ScubaThrower class
class ScubaThrower(ThrowerAnt):
    name = 'Scuba'
    food_cost = 6
    is_waterproof = True
    implemented = True
    
# END Problem 11


class QueenAnt(ThrowerAnt):
    """QueenAnt boosts the damage of all ants behind her.
    **QueenAnt（蚁后）提升她身后所有 Ant（蚂蚁）的伤害。**"""

    name = 'Queen'
    food_cost = 7
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 12
    implemented = True   # Change to True to view in the GUI
    # END Problem 12

    def action(self, gamestate):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.**蚁后会投掷一片叶子，但也会将她所在隧道中蚂蚁的伤害翻倍。**
        """
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        super().action(gamestate)
        cur_place = self.place.exit
        while cur_place:
            if cur_place.ant:
                cur_place.ant.double()
                if cur_place.ant.is_container and cur_place.ant.ant_contained:
                    cur_place.ant.ant_contained.double()
            cur_place = cur_place.exit
        # END Problem 12

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and if the QueenAnt has no health
        remaining, signal the end of the game.
        将生命值减少 AMOUNT；如果 QueenAnt（蚁后）没有剩余生命值，则发出游戏结束的信号。
        """
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        super().reduce_health(amount)
        if self.place == None:
            ants_lose()
        # END Problem 12


################
# Extra Challenge #
################

class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees.
    **一种会对 Bees（蜜蜂）造成 Slow（减速）效果的 ThrowerAnt（投掷蚁）。**"""

    name = 'Slow'
    food_cost = 6
    # BEGIN Problem EC 1
    implemented = False   # Change to True to view in the GUI
    # END Problem EC 1

    def throw_at(self, target):
        # BEGIN Problem EC 1
        "*** YOUR CODE HERE ***"
        # END Problem EC 1


class ScaryThrower(ThrowerAnt):
    """ThrowerAnt that intimidates Bees, making them back away instead of advancing.
    **一种威慑 Bees（蜜蜂）的 ThrowerAnt（投掷蚁），使它们后退而不是前进。**"""

    name = 'Scary'
    food_cost = 6
    # BEGIN Problem EC 2
    implemented = False   # Change to True to view in the GUI
    # END Problem EC 2

    def throw_at(self, target):
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"
        # END Problem EC 2


class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place.
    **NinjaAnt（忍者蚁）不阻挡路径，并对其所在 Place（地点）中的所有 Bee（蜜蜂）造成伤害。**"""

    name = 'Ninja'
    damage = 1
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem EC 3
    implemented = False   # Change to True to view in the GUI
    # END Problem EC 3

    def action(self, gamestate):
        # BEGIN Problem EC 3
        "*** YOUR CODE HERE ***"
        # END Problem EC 3


class LaserAnt(ThrowerAnt):
    """ThrowerAnt that damages all Insects standing in its path.
    **一种会对其路径上所有 Insect（昆虫）造成伤害的 ThrowerAnt（投掷蚁）。**"""

    name = 'Laser'
    food_cost = 10
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem EC 4
    implemented = False   # Change to True to view in the GUI
    # END Problem EC 4

    def __init__(self, health=1):
        super().__init__(health)
        self.insects_shot = 0

    def insects_in_front(self):
        # BEGIN Problem EC 4
        return {}
        # END Problem EC 4

    def calculate_damage(self, distance):
        # BEGIN Problem EC 4
        return 0
        # END Problem EC 4

    def action(self, gamestate):
        insects_and_distances = self.insects_in_front()
        for insect, distance in insects_and_distances.items():
            damage = self.calculate_damage(distance)
            insect.reduce_health(damage)
            if damage:
                self.insects_shot += 1


########
# Bees #
########

class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants.
    **一只 Bee（蜜蜂）沿着出口在各个 Place（地点）之间移动，并蜇刺 Ant（蚂蚁）。**"""

    name = 'Bee'
    damage = 1
    is_waterproof = True


    def sting(self, ant):
        """Attack an ANT, reducing its health by 1."""
        ant.reduce_health(self.damage)

    def move_to(self, place):
        """Move from the Bee's current Place to a new PLACE."""
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place.
        **如果这只 Bee（蜜蜂）无法前进到下一个 Place（地点），则返回 True。**"""
        # Special handling for NinjaAnt
        # BEGIN Problem EC 3
        return self.place.ant is not None
        # END Problem EC 3

    def action(self, gamestate):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.
        **一只 Bee（蜜蜂）的动作：如果它被阻挡，就蜇刺阻挡其出口的 Ant（蚂蚁）；
        否则，移动到其当前 Place（地点）的出口。**
        gamestate -- The GameState, used to access game state information.
        """
        destination = self.place.exit


        if self.blocked():
            self.sting(self.place.ant)
        elif self.health > 0 and destination is not None:
            self.move_to(destination)

    def add_to(self, place):
        place.bees.append(self)
        super().add_to( place)

    def remove_from(self, place):
        place.bees.remove(self)
        super().remove_from(place)

    def scare(self, length):
        """
        If this Bee has not been scared before, cause it to attempt to
        go backwards LENGTH times.
        **如果这只 Bee（蜜蜂）之前没有被吓退过，则使其尝试后退 LENGTH 次。**
        """
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"
        # END Problem EC 2


class Wasp(Bee):
    """Class of Bee that has higher damage.**具有更高伤害的 Bee（蜜蜂）类。**"""
    name = 'Wasp'
    damage = 2


class Boss(Wasp):
    """The leader of the bees. Damage to the boss by any attack is capped.
    **蜜蜂的首领。任何攻击对该 Boss 造成的伤害都有上限。**"""
    name = 'Boss'
    damage_cap = 8

    def reduce_health(self, amount):
        super().reduce_health(min(amount, self.damage_cap))


class Hive(Place):
    """The Place from which the Bees launch their assault.
    Bees（蜜蜂）发动进攻的 Place（地点）
    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """
    is_hive = True

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees():
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, gamestate):
        exits = [p for p in gamestate.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(gamestate.time, []):
            bee.move_to(random.choice(exits))
            gamestate.active_bees.append(bee)

###################
# Game Components #
###################

class GameState:
    """An ant collective that manages global game state and simulates time.
    **一个管理全局游戏状态并模拟时间的蚂蚁集体。**

    属性：
    - `time` —— 已流逝的时间
    - `food` —— 蚁群可用食物总量
    - `places` —— 蚁群中所有 Place（地点）的列表（包括一个 Hive 蜂巢）
    - `bee_entrances` —— 蜜蜂可以进入的 Place（地点）列表
    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, beehive, ant_types, create_places, dimensions, food=2):
        """Create an GameState for simulating a game.
        **创建一个用于模拟游戏的 GameState。**

        参数：
        - `beehive` —— 一个装满蜜蜂的 Hive（蜂巢）
        - `ant_types` —— 一个 Ant（蚂蚁）类的列表
        - `create_places` —— 一个用于创建 Place（地点）集合的函数
        - `dimensions` —— 一个包含游戏布局尺寸的二元组
        Arguments:
        beehive -- a Hive full of bees
        ant_types -- a list of ant classes
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        """
        self.time = 0
        self.food = food
        self.beehive = beehive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees = []
        self.configure(beehive, create_places)

    def configure(self, beehive, create_places):
        """Configure the places in the colony.配置 colony（蚁群/殖民地）中的各个 Place（地点）"""
        self.base = AntHomeBase('Ant Home Base')
        self.places = OrderedDict()
        self.bee_entrances = []

        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = beehive
                self.bee_entrances.append(place)
        register_place(self.beehive, False)
        create_places(self.base, register_place,
                      self.dimensions[0], self.dimensions[1])

    def ants_take_actions(self): # Ask ants to take actions
        for ant in self.ants:
            if ant.health > 0:
                ant.action(self)

    def bees_take_actions(self, num_bees): # Ask bees to take actions
        for bee in self.active_bees[:]:
            if bee.health > 0:
                bee.action(self)
            if bee.health <= 0:
                num_bees -= 1
                self.active_bees.remove(bee)
        if num_bees == 0: # Check if player won
            raise AntsWinException()
        return num_bees

    def simulate(self):
        """Simulate an attack on the ant colony. This is called by the GUI to play the game.
        **模拟一次对蚁群的攻击。此方法由 GUI 调用，用于进行游戏。**"""
        num_bees = len(self.bees)
        try:
            while True:
                self.beehive.strategy(self) # Bees invade from hive
                yield None # After yielding, players have time to place ants
                self.ants_take_actions()
                self.time += 1
                yield None # After yielding, wait for throw leaf animation to play, then ask bees to take action
                num_bees = self.bees_take_actions(num_bees)
        except AntsWinException:
            print('All bees are vanquished. You win!')
            yield True
        except AntsLoseException:
            print('The bees reached homebase or the queen ant queen has perished. Please try again :(')
            yield False

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.
        **如果有足够的食物，就放置一只 Ant（蚂蚁）。**

        **此方法由当前策略调用，用于部署蚂蚁。**
        This method is called by the current strategy to deploy ants.
        """
        ant_type = self.ant_types[ant_type_name]
        if ant_type.food_cost > self.food:
            print('Not enough food remains to place ' + ant_type.__name__)
        else:
            ant = ant_type()
            self.places[place_name].add_insect(ant)
            self.food -= ant.food_cost
            return ant

    def remove_ant(self, place_name):
        """Remove an Ant from the game."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status


class AntHomeBase(Place):
    """AntHomeBase at the end of the tunnel, where the queen normally resides.
    **AntHomeBase（蚂蚁大本营）位于隧道末端，蚁后通常居住在那里。**"""

    def add_insect(self, insect):
        """Add an Insect to this Place.
        将一只 Insect（昆虫）添加到此 Place（地点）。

        实际上不能将 Ant（蚂蚁）添加到 AntHomeBase（蚂蚁大本营）。但是，如果一只 Bee（蜜蜂）
        试图进入 AntHomeBase，则会抛出 AntsLoseException，表示游戏结束。
        Can't actually add Ants to a AntHomeBase. However, if a Bee attempts to
        enter the AntHomeBase, a AntsLoseException is raised, signaling the end
        of a game.
        """
        assert isinstance(insect, Bee), 'Cannot add {0} to AntHomeBase'
        raise AntsLoseException()


def ants_win():
    """Signal that Ants win."""
    raise AntsWinException()


def ants_lose():
    """Signal that Ants lose."""
    raise AntsLoseException()


def ant_types():
    """Return a list of all implemented Ant classes
    **返回所有已实现的 Ant（蚂蚁）类的列表。**"""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]


def bee_types():
    """Return a list of all implemented Bee classes."""
    all_bee_types = []
    new_types = [Bee]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_bee_types.extend(new_types)
    return all_bee_types


class GameOverException(Exception):
    """Base game over Exception.**游戏结束异常的基类。**"""
    pass


class AntsWinException(GameOverException):
    """Exception to signal that the ants win.**用于表示 Ant（蚂蚁）获胜的异常。**"""
    pass


class AntsLoseException(GameOverException):
    """Exception to signal that the ants lose."""
    pass


###########
# Layouts #
###########


def wet_layout(queen, register_place, tunnels=3, length=9, moat_frequency=3):
    """Register a mix of wet and and dry places.注册一组干湿混合的 Place（地点）"""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)


def dry_layout(queen, register_place, tunnels=3, length=9):
    """Register dry tunnels.**注册干燥隧道。**"""
    wet_layout(queen, register_place, tunnels, length, 0)


#################
# Assault Plans #
#################

class AssaultPlan(dict):
    """The Bees' plan of attack for the colony.  Attacks come in timed waves.
    **Bees（蜜蜂）对 colony（蚁群/殖民地）的进攻计划。攻击以定时波次到来。**

    **AssaultPlan 是一个字典，从时间（int）映射到波次（Bee 的列表）。**
    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def add_wave(self, bee_type, bee_health, time, count):
        """Add a wave at time with count Bees that have the specified health.
        **在 time 时刻添加一个波次，包含 count 只具有指定 health（生命值）的 Bee（蜜蜂）。**"""
        bees = [bee_type(bee_health) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    def all_bees(self):
        """Place all Bees in the beehive and return the list of Bees.
        **将所有 Bee（蜜蜂）放入 Hive（蜂巢），并返回 Bee 的列表。**"""
        return [bee for wave in self.values() for bee in wave]