import numpy as np
from skimage import measure
from sklearn.neighbors import NearestNeighbors
from skullFindSurface import getSurfaceVoxels


def findSurfaceNormals(surfaceVoxels, voxelData, ConstPixelSpacing):
    # Takes in verts, normals from the Marching Cubes Algorithm
    verts, normals, _ = getSurfaceMesh(voxelData, ConstPixelSpacing)

    surfelCoord = np.float64(surfaceVoxels) * ConstPixelSpacing

    nbrs = NearestNeighbors(n_neighbors=1, algorithm='kd_tree').fit(verts)
    distances, indices = nbrs.kneighbors(surfelCoord)
    surfaceNormals = normals[indices[:]]
    surfaceNormals = surfaceNormals.reshape(
        surfaceNormals.shape[0], surfaceNormals.shape[2])

    surfaceNormals, surfelCoord = getOutwardNormals(
        surfaceNormals, surfelCoord)

    return surfelCoord, surfaceNormals


def getSurfaceMesh(voxelData, ConstPixelSpacing):
    verts, faces, normals, values = measure.marching_cubes_lewiner(
        voxelData, 0, ConstPixelSpacing)
    return verts, normals, faces


def getOutwardNormals(normals, surfels):
    # Takes in all normals and returns only outward normals for the skull
    # Returns a point roughly at the center of the skull
    mid = np.average(surfels, 0)
    diff_coord = surfels - mid
    thresh = -1/np.sqrt(2)
    outward_normals = normals[np.sum(diff_coord * normals, 1) > thresh]
    outer_surfels = surfels[np.sum(diff_coord * normals, 1) > thresh]

    return outward_normals, outer_surfels
