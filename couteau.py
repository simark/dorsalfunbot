from PIL import Image
from PIL import ImageDraw
import sys

# left, up, right, low
def extractRect(im, box, filename):
    region = im.crop(box)
    region.save(filename)
    

def floodfill(image, xy, value, border=None):
    "Fill bounded region."
    # based on an implementation by Eric S. Raymond
    pixel = image.load()    
    x, y = xy
    
    max_x = x
    min_x = x
    max_y = y
    min_y = y
    

    background = pixel[x, y]
    if background == value:
        raise ValueError()
    pixel[x, y] = value

    edge = [(x, y)]

    while edge:
        newedge = []
        for (x, y) in edge:
            for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                try:
                    p = pixel[s, t]
                except IndexError:
                    pass
                else:
                    if p == background:
                        max_x = max(max_x, s)
                        min_x = min(min_x, s)
                        max_y = max(max_y, t)
                        min_y = min(min_y, t)
                        pixel[s, t] = value
                        newedge.append((s, t))
        edge = newedge
        
    return (min_x, min_y, max_x, max_y)

def decouper(nomFichier):
    point = (0, 0)

    im = Image.open(nomFichier)
    imOrig = im.copy()

    im = im.convert("RGB")

    prev_max_y = 0
    prev_max_x = 0

    x_inc = 4
    y_inc = 4

    for jour in ['titre', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']:
        prev_max_y = 0
        point = (prev_max_x + x_inc, 0)
        
        for case in range(7):
            point = (point[0], prev_max_y + y_inc)
        
            #print point
            box = floodfill(im, point, (255, 0, 0))
            #print box
            extractRect(imOrig, box, jour + str(case) + ".bmp")
            
            prev_max_y = box[3]
            prev_max_x = box[2]
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Quel cave!")
    else:
        decouper(sys.argv[1])
