from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import gridspec


def colorPalette(link):
    original = Image.open(link)
    img = original.copy()

    img = Image.open(link)
    reduced = img.convert('P', palette=Image.ADAPTIVE, colors=5)

    palette = reduced.getpalette()
    palette = [[palette[c]/255, palette[c+1]/255, palette[c+2]/255] for c in range(0,len(palette),3) if palette[c] != 0]


    fig = plt.figure()
    spec = gridspec.GridSpec(ncols=2, nrows=1,width_ratios=[2, 1])

    # Original image
    fig.add_subplot(spec[0])
    plt.title("Reference Image")
    plt.imshow(img)

    # Color Palette
    y = [i for i in range(len(palette))]
    x= [10 for i in range(len(palette))] 

    fig.add_subplot(spec[1])
    plt.title("Color palette")
    plt.barh(y, x, color=palette)
    plt.axis('off')

    plt.show()
    # plt.savefig("Palette.png")

    return palette




# p = colorPalette("1.jpg")