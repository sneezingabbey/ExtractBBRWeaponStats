import os
import json
import datetime
import time
from tkinter import Tk, filedialog

categories = {
    "Assault Rifles": ["AK74", "M4A1", "AK15", "SCAR-H", "AUG_A3", "SG550", "FAMAS", "ACR", "G36C", "HK419", "FAL", "AK5C"],

    "Submachine Guns": ["MP7", "UMP-45", "PP2000", "PP19", "Kriss_Vector", "MP5"],

    "Personal Defense Weapons": ["Honey_Badger", "Groza", "P90"],

    "Carbines": ["As_Val", "ScorpionEVO"],

    "Light Support Guns": ["L86A1", "MG36"],

    "Light Machine Guns": ["M249", "Ultimax100"],

    "Designated marksman Rifles": ["MK20", "M110", "MK14_EBR", "SVD"],

    "Sniper Rifles": ["SSG_69", "SV-98", "L96", "Rem700", "M200", "MSR"],

    "Pistols": ["M9", "MP_443", "USP"],

    "Automatic Pistols ": ["Glock_18"],

    "Heavy Caliber Pistols ": ["Unica", "Desert_Eagle", "Rsh12"]
}


def extract_asset_data(directory_path):
    weapons_data = {}

    for filename in os.listdir(directory_path):
        if "_" in filename and filename.endswith(".asset"):
            with open(os.path.join(directory_path, filename), 'r') as file:
                content = file.readlines()

            weapon_name = filename.split("_", 1)[1].replace(".asset", "")
            data_keys = [
                "DamageOnInfantryBody", "DamageOnLightArmoredVehicles", "DamageOnHeavyHeavyVehicles",
                "BulletVelocity", "ProjectileVisualSize", "BaseHipFireAccuracy", "VerticalMouse",
                "HorizontalMouse", "FirstShotRecoil", "AdsTime", "PlayerRunningSpeed",
                "ReloadSpeed", "DrawSpeed", "RoundsPerMinute", "ShotSoundDistance"
            ]

            weapon_data = {}
            for key in data_keys:
                for line in content:
                    if key + ": " in line:
                        # Convert all attributes to integers
                        value = line.split(": ")[1].strip()
                        if '.' in value:
                            weapon_data[key] = float(value)
                        else:
                            weapon_data[key] = int(value)
                        break

            # Check if any key is missing from the extracted weapon data
            if all(key in weapon_data for key in data_keys):
                weapons_data[weapon_name] = weapon_data
                print(weapon_name)

    return weapons_data


def main():
    Tk().withdraw()  # Hide the root tkinter window
    print("Please select the MonoBehaviour Asset Folder, that was dumped by AssetRipper")
    directory_path = filedialog.askdirectory(
        title="Select the MonoBehaviour Asset Folder")

    if not directory_path:
        print("No directory selected. Exiting.")
        time.sleep(3)
        return

    weapons_data = extract_asset_data(directory_path)

    weapon_count = len(weapons_data)

    categorized_weapons = {}
    for category, weapons in categories.items():
        categorized_weapons[category] = {}
        for weapon in weapons:
            if weapon in weapons_data:
                categorized_weapons[category][weapon] = weapons_data[weapon]
            else:
                print(
                    f"Weapon '{weapon}' from category '{category}' not found in weapons_data!")

    categorized_weapon_count = sum(len(weapons)
                                   for weapons in categorized_weapons.values())

    output_data = {
        'update_version': "2.0.2",
        'dump_date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'weapon_count': weapon_count,
        'weapon_categories' : len(categorized_weapons),
        'categorized_weapon_count': categorized_weapon_count,
        'weapon_categories': categorized_weapons
    }

    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_filename = "weapons_data.json"
    with open(os.path.join(script_directory, output_filename), 'w') as json_file:
        json.dump(output_data, json_file, indent=4)

    print(f"{weapon_count} weapons had their data extracted!")

    print("Extraction complete!")
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
