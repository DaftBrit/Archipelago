import string

from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld

from . import Options, Items, Locations, Regions, Rules, Events
from .Options import noita_options

# TODO: Gate holy mountain access behind an event that triggers when you visit the same holy mountain?


class NoitaWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Noita integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["DaftBrit"]
    )]
    theme = "partyTime"


# Keeping World slim so that it's easier to comprehend
class NoitaWorld(World):
    """
    Noita is a magical action roguelite set in a world where every pixel is physically simulated. Fight, explore, melt,
    burn, freeze, and evaporate your way through the procedurally generated world using wands you've created yourself.
    """
    game: str = "Noita"
    option_definitions = Options.noita_options
    topology_present = True

    item_name_to_id = Items.item_name_to_id
    location_name_to_id = Locations.location_name_to_id

    item_name_groups = Items.item_name_groups

    data_version = 1
    web = NoitaWeb()

    def get_option(self, name):
        return getattr(self.multiworld, name)[self.player].value

    # Returned items will be sent over to the client
    def fill_slot_data(self):
        slot_data = {
            "seed": self.multiworld.seed_name,
        }

        for option_name in self.option_definitions:
            slot_data[option_name] = self.get_option(option_name)

        return slot_data

    def create_regions(self) -> None:
        Regions.create_all_regions_and_connections(self.multiworld, self.player)

    def create_items(self) -> None:
        Items.create_all_items(self.multiworld, self.player)

    def set_rules(self) -> None:
        Rules.create_all_rules(self.multiworld, self.player)

    # Generate victory conditions and other shenanigans
    def generate_basic(self) -> None:
        Events.create_all_events(self.multiworld, self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(Items.filler_items)