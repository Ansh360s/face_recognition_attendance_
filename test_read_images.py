import os
path="images"

folders=os.listdir(path)

print("folders:",folders)

for folder in folders:
    folder_path=os.path.join(path,folder)

    print("\nInside:",folder)

    images = os.listdir(folder_path)

    for img in images:
        print(" ",img)