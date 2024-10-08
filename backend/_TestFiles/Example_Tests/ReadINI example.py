
import configparser
config = configparser.ConfigParser()

config.read("/home/jaffator/I2C/Config.INI")
areas_dict = {}
digitalpin_dict = {}
section_digitalPins = "DigitalPins"
section_areas = "Areas"


# Procedura bude muset být spuštěna na začátku spuštění alarmu aby se inicioval dictionary digitalpin_dict
def create_dicts():
    for dig_key in config["DigitalPins"]:
        digitalpin_dict[dig_key] = int(config[section_digitalPins][dig_key])
    for area_key in config[section_areas]:
        temp_list = []
        for item in config[section_areas][area_key].split(","):
            temp_list.append(digitalpin_dict[item])
        areas_dict[area_key] = temp_list


def selected_areas(self, list_of_areas: list):
    self.
    dig_list = []
    for x in list_of_areas:
        dig_list += areas_dict[x]
    return dig_list


what_alarm = ["patro"]
create_dicts()
print(selected_areas(what_alarm))
