import numpy
from PIL import Image

base_10_colors = [
    (0,0,0),
    (255,255,255),
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (192,192,192),
    (128,128,128)
]

def generate_base_10_random():
    with open("demo_random.csv", "w") as test:
        rng = numpy.random.default_rng(1994)
        arr = rng.integers(low=0, high=10, size=1048576)
        for i in arr:
            test.write(str(i)+"\n")

def generate_tricky_base_10():
    with open("demo_tricky.csv", "w") as test:
        rng = numpy.random.default_rng(1994)
        arr = rng.integers(low=0, high=10, size=1048576)
        for i in range(1024*67, 1024*89):
            arr[i] = 2
        for i in range(1024*147, 1024*180):
            arr[i] = 2
        for i in range(1024*363, 1024*427):
            arr[i] = 2
        for i in range(1024*490, 1024*540):
            arr[i] = 2
        for i in range(1024*700, 1024*740):
            arr[i] = 2
        for i in range(1024*920, 1024*950):
            arr[i] = 2
        for i in arr:
            test.write(str(i)+"\n")


def generate_champernaum_base_10():
    with open("demo_champernaum.csv", "w") as test:
        with open("todas_las_secuencias.csv", "r") as source:
            i = 0
            for line in source:
                test.write(str(line[0])+"\n")
                i+=1
                if i == 1024*1024:
                    break

def make_image_base_10():
    array = []
    with open("demo_champernaum.csv", "r") as test:
        for line in test:
            array.append(int(line[0]))
    print(len(array))
    imgArray = []
    for i in range(1024):
        row = []
        for j in range(1024):
            row.append(base_10_colors[array[1024*i + j]])
        imgArray.append(row)

    imagen = numpy.array(imgArray, dtype=numpy.uint8)

    new_image = Image.fromarray(imagen)
    new_image.save('demo_champernaum.png')

#generate_base_10_random()
#make_image_base_10()

# generate_tricky_base_10()
# make_image_base_10()

generate_champernaum_base_10()
make_image_base_10()



# m=13 para collision
# m=20 para gap
