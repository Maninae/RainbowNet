from PIL import Image
import sys
import os
import urllib

source_path = 'gifs_data'

path = os.path.join('..', 'data')
if not os.path.exists(path):
    os.makedirs(path)

def process_gif(infile):
    try:
        image = Image.open(infile)
    except IOError:
        print "Can't load", infile
        sys.exit(1)
    palette = image.getpalette()
    name = os.path.split(infile)[-1].split('.')[0]

    save_dir = os.path.join(path, name)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        i = 0
        while True:
            image.putpalette(palette)
            new_image = Image.new("RGBA", image.size)
            new_image.paste(image)
            new_image.save(os.path.join(save_dir, str(i) + "-" + name + '.png'))

            i += 1
            image.seek(image.tell() + 1)

    except EOFError:
        pass # end of sequence

# Call process_gif_list() to download 50 gifs from list
def process_gif_list():
    gifs_list = "gifs_list.tsv"
    with open(gifs_list, 'r') as file:
        lines = file.readlines()
    counter = 1
    for line in lines:
        url = line.split()[0]
        name = "gif" + str(counter) + ".gif"
        image = urllib.urlretrieve(url, name)
        process_gif(name)

        if counter == 50:
            break
        counter += 1

# Process all files in gifs_data directory
for file in os.listdir(source_path):
    process_gif(os.path.join(source_path, file))
