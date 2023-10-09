from os.path import isfile
from shutil import copyfile


'''
A patching script for medieval 2 hotseats that allows logging in into any
faction without needing to know their passwords and using the console without
providing a password, even if the console was disabled in the hotseat.

Basically how it works is it modifies if conditions that check whether the passwords
are similar or not(or their hashes) and continue regardless of the comparison results.
'''

PATCHES = [
    {
        "74 7c 8d 44 24 28 68 e4 00 00 00 50 e8 38 48 e9":
        "eb 7c 8d 44 24 28 68 e4 00 00 00 50 e8 38 48 e9"
    },
    {
        "75 19 8b 44 24 10 50 68 20 77 3d 01 e8 bc fb ff":
        "eb 19 8b 44 24 10 50 68 20 77 3d 01 e8 bc fb ff"
    },
    {
        "75 25 8b 4c 24 18 51 68 14 b9 3d 01 e8 8e 8a ff":
        "eb 25 8b 4c 24 18 51 68 14 b9 3d 01 e8 8e 8a ff"
    },
    {
        "75 11 8b 44 24 18 50 68 e0 b8 3d 01 e8 3d 8a ff":
        "eb 11 8b 44 24 18 50 68 e0 b8 3d 01 e8 3d 8a ff"
    },
    {
        "74 11 8b 4c 24 18 51 68 98 b8 3d 01 e8 f6 89 ff":
        "eb 11 8b 4c 24 18 51 68 98 b8 3d 01 e8 f6 89 ff"
    },
]

# Checks whether the orignal bytes are present or not
def fileCheck(filename):
    data = ''
    with open(filename, 'rb') as input_file:
        data = input_file.read()
    for patch in PATCHES:
        for original_bytes in patch.keys():
            if data.find(bytearray.fromhex(original_bytes)) == -1:
                return False
    return True

def apply_patches(filename):
    data = ''
    with open(filename, 'rb') as input_file:
        data = input_file.read()

    for patch in PATCHES:
        for key, value in patch.items():
            data = data.replace(bytearray.fromhex(key), bytearray.fromhex(value))

    with open(filename, "wb") as output_file:
        output_file.write(data)
        
def main():
    if(not isfile("medieval2.exe")):
        raise SystemExit(
            "medieval2.exe not found, make sure the file exists in the same folder/directory")
    elif(not isfile("medieval2_backup.exe")):
        copyfile("medieval2.exe", "medieval2_backup.exe")
        print("Made a copy of medieval2.exe")

    if(not fileCheck("medieval2.exe")):
        raise SystemExit(
            "medieval2.exe is not the original file, can't apply the patches")
    else:
        apply_patches("medieval2.exe")
        print("medieval2.exe patched successfully")


if __name__ == "__main__":
    main()
