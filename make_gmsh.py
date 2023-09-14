import numpy as np
import gmsh
import h5py


file = h5py.File("Voxelized.hdf5")

dims = tuple(file['VoxelDataContainer']["DIMENSIONS"])
spacing = tuple(file['VoxelDataContainer']["SPACING"])
grain_ids = np.array(
            file['VoxelDataContainer']["CELL_DATA"]["GrainIds"])
grains = np.unique(grain_ids)
np.sort(grains)

gmsh.initialize()
gmsh.model.add("m1")

point_number = lambda _i, _j, _k: int(_i + dims[1] * (_j + dims[2] * _k))

for i in range(dims[0]):
    for j in range(dims[1]):
        for k in range(dims[2]):
            gmsh.model.geo.addPoint(i*spacing[0], 
                                    j*spacing[1], 
                                    k*spacing[2],
                                    tag=point_number(i,j,k))
            print(f"(i,j,k) = ({i,j,k})")
            if i > 0:
                gmsh.model.geo.addLine(point_number(i-1,j,k), 
                                        point_number(i,j,k))
            if j > 0:
                gmsh.model.geo.addLine(point_number(i,j-1,k), 
                                        point_number(i,j,k))
            if k > 0:
                gmsh.model.geo.addLine(point_number(i,j,k-1), 
                                        point_number(i,j,k))
print("Begining Synchronization...")
gmsh.model.geo.synchronize()
print("Synchronization Complete!")
for grain_number in grains:
    print(f"Adding Group: var_{grain_number}")
    grain_points = np.argwhere(grain_ids==grain_number).flatten().tolist()
    gmsh.model.addPhysicalGroup(0, grain_points, name=f"var_{grain_number}")
    
import pdb;pdb.set_trace()
