import copy
from enum import IntEnum
import io
import re


class Faction:
    """Represents either the immune system or the infection"""

    def __init__(self, armies):
        self.armies = armies

    @classmethod
    def from_str(self, input_str):
        buf = io.StringIO(input_str)
        buf.readline()  # discard header

        armies = []

        for line in buf.readlines():
            army = Army.from_str(line.strip())
            armies.append(army)

        return Faction(armies)

    def choose_tagets(self, other_faction):

        # target lists are tuples. 0 is attacking army, 1 is target army
        return_list = []

        #  go in decreasing order of effective power choosing targets; in a
        #  tie, the army with the higher initiative chooses first
        my_armies = copy.copy(self.armies)
        my_armies = sorted(my_armies,
                           key=lambda army: (army.get_effective_power(), army.initiative),
                           reverse=True)

        other_armies = copy.copy(other_faction.armies)

        for my_army in my_armies:

            # we want to target the opposing army that my_army can do the most
            # damage to
            other_armies = sorted(other_armies,
                                  key=lambda other_army: (other_army.get_damage_taken(my_army), other_army.get_effective_power(), other_army.initiative),
                                  reverse=True)
            if len(other_armies) > 0:
                other_army = other_armies[0]

                damage_dealt = other_army.get_damage_taken(my_army)
                if damage_dealt > 0:
                    return_list.append((my_army, other_army))
                    other_armies.remove(other_army)

        return return_list

    def clean_up_dead_units(self):
        remaining_armies = []

        for army in self.armies:
            if army.units > 0:
                remaining_armies.append(army)
        self.armies = remaining_armies

    def units_remaining(self):
        count = 0
        for army in self.armies:
            count += army.units
        return count

    def give_boost(self, boost):
        for army in self.armies:
            army.attack_power += boost


class Element(IntEnum):
    Fire = 1
    Slashing = 2
    Cold = 3
    Radiation = 4
    Bludgeoning = 5

    @classmethod
    def from_str(self, input_str):
        if input_str == 'fire':
            return Element.Fire
        elif input_str == 'slashing':
            return Element.Slashing
        elif input_str == 'cold':
            return Element.Cold
        elif input_str == 'radiation':
            return Element.Radiation
        elif input_str == 'bludgeoning':
            return Element.Bludgeoning
        else:
            print(f'Unexpected element: {input_str}')


class Army:
    def __init__(self, attack_type, immunities, weaknesses,
                 hp, units, attack_power, initiative):
        self.attack_type = attack_type
        self.immunities = immunities
        self.weaknesses = weaknesses

        self.hp = hp
        self.units = units
        self.attack_power = attack_power
        self.initiative = initiative

    def get_effective_power(self):
        return self.units * self.attack_power

    def get_damage_taken(self, attacking_army):
        attack_element = attacking_army.attack_type
        is_weak = attack_element in self.weaknesses
        is_immune = attack_element in self.immunities

        if is_immune:
            damage = 0
        else:
            damage = attacking_army.get_effective_power()
            if is_weak:
                damage *= 2

        return damage


    @classmethod
    def from_str(self, input_str):
        units = int(re.search(r'\d+', input_str).group(0))
        hp = int(re.search(r'\d+(?= hit)', input_str).group(0))
        attack_power = int(re.search(r'(?<=does )\d+', input_str).group(0))
        initiative = int(re.search(r'(?<=initiative )\d+', input_str).group(0))

        attack_type_str = re.search(r'\w+(?= damage)', input_str).group(0)
        attack_type = Element.from_str(attack_type_str)

        # weak to up to two things
        weaknesses = []
        weakness_idx = input_str.find('weak to')
        if weakness_idx != -1:
            weakness_idx += len('weak to ')
            weakness_tokens = input_str[weakness_idx:].split(' ')

            char_after_weakness = input_str[weakness_idx + len(weakness_tokens[0])-1]
            weakness_str = weakness_tokens[0][:-1]
            weaknesses.append(Element.from_str(weakness_str))
            if char_after_weakness == ',':
                weaknesses.append(Element.from_str(weakness_tokens[1][:-1]))

        # immune to up to two things
        immunities = []
        immunity_idx = input_str.find('immune to')
        if immunity_idx != -1:
            immunity_idx += len('immune to ')
            immunity_tokens = input_str[immunity_idx:].split(' ')

            char_after_immunity = input_str[immunity_idx + len(immunity_tokens[0])-1]
            immunity_str = immunity_tokens[0][:-1]
            immunities.append(Element.from_str(immunity_str))
            if char_after_immunity == ',':
                immunities.append(Element.from_str(immunity_tokens[1][:-1]))

        return Army(attack_type, immunities, weaknesses, hp,
                    units, attack_power, initiative)

    def __repr__(self):
        return_str = ''
        return_str += f'EP: {self.get_effective_power()} Units: {self.units}, HP: {self.hp}, AttackType: {self.attack_type} AP: {self.attack_power} initiative {self.initiative} Weak: {self.weaknesses} Immune: {self.immunities}'

        return return_str


def selection_phase(immune_system_faction, infection_faction):

    # target lists are tuples. 0 is attacking army, 1 is target army
    immune_system_targets = immune_system_faction.choose_tagets(infection_faction)
    infection_targets = infection_faction.choose_tagets(immune_system_faction)

    # put all the targets into one list for sorting into who gets to attack when
    immune_system_targets.extend(infection_targets)
    targets = immune_system_targets

    # sort in decreasing order of initiative
    targets = sorted(targets,
                     key=lambda target: target[0].initiative,
                     reverse=True)

    return targets


def attack_phase(targets, immune_system_faction, infection_faction):
    for attacking_army, defending_army in targets:
        if attacking_army.units <= 0:
            continue

        damage_dealt = defending_army.get_damage_taken(attacking_army)

        defending_army.units -= damage_dealt // defending_army.hp

    infection_faction.clean_up_dead_units()
    immune_system_faction.clean_up_dead_units()


def main():
    input_str = open('input/Day24.txt').read()
#    input_str = open('test/day24_ex.txt').read()
    components = input_str.split('\n\n')
    top_str = components[0]
    bottom_str = components[1]

    immune_system_faction = Faction.from_str(top_str)
    immune_system_faction.give_boost(35)  # set to 0 for part 1, adjust for part 2 until immune system wins
    infection_faction = Faction.from_str(bottom_str)

    round = 0
    while immune_system_faction.units_remaining() > 0 and infection_faction.units_remaining() > 0:
        # target list is tuples. 0 is attacking army, 1 is target army
        targets = selection_phase(immune_system_faction, infection_faction)
        attack_phase(targets, immune_system_faction, infection_faction)

        immune_units_remaining = immune_system_faction.units_remaining()
        infection_units_remaining = infection_faction.units_remaining()
        round += 1

    print(f'Immune system units remaining: {immune_units_remaining}')
    print(f'Infection system units remaining: {infection_units_remaining}')


if __name__ == "__main__":
    main()

# 20410 too high
