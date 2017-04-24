from pirs.solids import Box
from rod_models import pin, ifba, tube, chan
from rod_models import ap, ah, pp
from assembly_map import map_dict

# 1

# Number of rod rows and columns:
Nx = 17
Ny = Nx

# 2

model = Box(Z=ah + 2*ap)
model.X = Nx*pp - 0.000001
model.Y = Ny*pp - 0.000001

model.material = 'water'
model.temp.set_values(580.)
model.dens.set_values(1.)

model.grid.x = pp
model.grid.y = pp
model.grid.z = model.Z

model.temp.prec = 50. 
model.dens.prec = 0.002

# 3

# prepare rods
rods = []
for j in range(Ny):
    for i in range(Nx):
        rod_type = map_dict[(i,j)]
        if rod_type == 'u':
            key = 'pin {0},{1}'
            rod = pin.copy_tree()
        elif rod_type == 'i':
            key = 'ifba {0},{1}'
            rod = ifba.copy_tree()
        elif rod_type == 'g':
            key = 'tube {0},{1}'
            rod = tube.copy_tree()
        elif rod_type == 'c':
            key = 'tube {0},{1}'
            rod = chan.copy_tree()
        key = key.format(i,j)
        rod.name = key
        rods.append(rod)

# insert rods to the model:
rod_keys = []
for j in range(Ny):
    for i in range(Nx):
        rod = rods.pop(0)
        model.grid.insert((i,j,0), rod)
        rod_keys.append(rod.get_key())

# put lattice to center:
model.grid.center()


