import itertools
from typing import Dict, NamedTuple, Optional, List, Set
from BaseClasses import Item, ItemClassification, MultiWorld
from . import Options


class ItemData(NamedTuple):
    code: Optional[int]
    group: str
    classification: ItemClassification = ItemClassification.progression
    required_num: int = 0


class NoitaItem(Item):
    game: str = "Noita"


def create_item(player: int, name: str) -> Item:
    item_data = item_table[name]
    return NoitaItem(name, item_data.classification, item_data.code, player)


def create_all_items(world: MultiWorld, player: int) -> None:
    sum_locations = len(world.get_unfilled_locations(player))

    # Generate fixed item pool, these are items with a specific fixed quantity that must be added
    itempool: List = []
    for item_name, count in required_items.items():
        itempool += [item_name] * count

    # Generate items based on victory condition settings (Orbs)
    vic = world.victory_condition[player].value
    orb_count = 0

    if vic == Options.VictoryCondition.option_pure_ending:
        orb_count = 11
    if vic == Options.VictoryCondition.option_peaceful_ending:
        orb_count = 33

    for i in range(orb_count):
        itempool += ["Orb"]

    if world.bosses_as_checks[player].value >= Options.BossesAsChecks.option_all_bosses:
        itempool += ["Perk (Spatial Awareness)"]

    # Create any non-progression repeat items (referred to as junk regardless of whether it's useful)
    filler_pool = filler_weights.copy()
    if world.bad_effects[player].value == 0:
        del filler_pool["Trap"]
    random_count = sum_locations - len(itempool)

    itempool += world.random.choices(
        population=list(filler_pool.keys()),
        weights=list(filler_pool.values()),
        k=random_count
    )

    # Convert itempool into real items
    world.itempool += [create_item(player, name) for name in itempool]


# 110000 - 110021
item_table: Dict[str, ItemData] = {
    "Trap":                                 ItemData(110000, "Traps", ItemClassification.trap),
    "Extra Max HP":                         ItemData(110001, "Pickups", ItemClassification.useful),
    "Spell Refresher":                      ItemData(110002, "Pickups", ItemClassification.filler),
    "Potion":                               ItemData(110003, "Items", ItemClassification.filler),
    "Gold (200)":                           ItemData(110006, "Gold", ItemClassification.filler),
    "Gold (1000)":                          ItemData(110007, "Gold", ItemClassification.filler),
    "Wand (Tier 1)":                        ItemData(110008, "Wands", ItemClassification.useful),
    "Wand (Tier 2)":                        ItemData(110009, "Wands", ItemClassification.useful),
    "Wand (Tier 3)":                        ItemData(110010, "Wands", ItemClassification.useful),
    "Wand (Tier 4)":                        ItemData(110011, "Wands", ItemClassification.useful),
    "Wand (Tier 5)":                        ItemData(110012, "Wands", ItemClassification.useful),
    "Wand (Tier 6)":                        ItemData(110013, "Wands", ItemClassification.useful),
    "Perk (Fire Immunity)":                 ItemData(110014, "Perks", ItemClassification.progression, 1),
    "Perk (Toxic Immunity)":                ItemData(110015, "Perks", ItemClassification.progression, 1),
    "Perk (Explosion Immunity)":            ItemData(110016, "Perks", ItemClassification.progression, 1),
    "Perk (Melee Immunity)":                ItemData(110017, "Perks", ItemClassification.progression, 1),
    "Perk (Electricity Immunity)":          ItemData(110018, "Perks", ItemClassification.progression, 1),
    "Perk (Tinker with Wands Everywhere)":  ItemData(110019, "Perks", ItemClassification.progression, 1),
    "Perk (All-Seeing Eye)":                ItemData(110020, "Perks", ItemClassification.progression, 1),
    "Perk (Extra Life)":                    ItemData(110021, "Repeatable Perks", ItemClassification.useful),
    "Orb":                                  ItemData(110022, "Orbs", ItemClassification.progression_skip_balancing),
    "Random Potion":                        ItemData(110023, "Items", ItemClassification.filler),
    "Secret Potion":                        ItemData(110024, "Items", ItemClassification.filler),
    "Chaos Die":                            ItemData(110025, "Items", ItemClassification.filler),
    "Greed Die":                            ItemData(110026, "Items", ItemClassification.filler),
    "Kammi":                                ItemData(110027, "Items", ItemClassification.filler),
    "Refreshing Gourd":                     ItemData(110028, "Items", ItemClassification.filler),
    "Sädekivi":                             ItemData(110029, "Items", ItemClassification.filler),
    "Broken Wand":                          ItemData(110030, "Items", ItemClassification.filler),
    "Powder Pouch":                         ItemData(110031, "Items", ItemClassification.filler),
    "Perk (Spatial Awareness)":             ItemData(110032, "Perks", ItemClassification.progression)
}

filler_weights: Dict[str, int] = {
    "Trap":             15,
    "Extra Max HP":     25,
    "Spell Refresher":  20,
    "Potion":           40,
    "Gold (200)":       15,
    "Gold (1000)":      6,
    "Wand (Tier 1)":    10,
    "Wand (Tier 2)":    8,
    "Wand (Tier 3)":    7,
    "Wand (Tier 4)":    6,
    "Wand (Tier 5)":    5,
    "Wand (Tier 6)":    4,
    "Perk (Extra Life)": 10,
    "Random Potion":    9,
    "Secret Potion":    10,
    "Chaos Die":        4,
    "Greed Die":        4,
    "Kammi":            4,
    "Refreshing Gourd": 4,
    "Sädekivi":         3,
    "Broken Wand":      10,
    "Powder Pouch":     10,
}


# These helper functions make the comprehensions below more readable
def get_item_group(item_name: str) -> str:
    return item_table[item_name].group


def item_is_filler(item_name: str) -> bool:
    return item_table[item_name].classification == ItemClassification.filler


def item_is_perk(item_name: str) -> bool:
    return item_table[item_name].group == "Perks"


filler_items: List[str] = list(filter(item_is_filler, item_table.keys()))
item_name_to_id: Dict[str, int] = {name: data.code for name, data in item_table.items()}

item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names)
    for group, item_names in itertools.groupby(item_table, get_item_group)
}

required_items: Dict[str, int] = {
    name: data.required_num
    for name, data in item_table.items() if data.required_num > 0
}
