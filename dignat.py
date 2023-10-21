import colour
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("dark_background")

class Camera:
    def __init__(cam, name, storage, matrix):
        # Camera name.
        cam.name = name

        # Storage (or at least matrix target) primaries.
        cam.storage = storage

        # Sensor to storage primaries matrix.
        cam.matrix = matrix

CAMERA_MATRICES = [
    Camera("ARRI Alexa", "Alexa Wide Gamut", np.array([[1.16568936, -0.18400079, 0.01831143], [-0.0524356, 1.01472615, 0.03770945], [0.0270692, -0.24782896, 1.22075976]])),
    Camera("Sony A7", "ITU-R BT.709", np.array([[1.93, -0.79, -0.14], [-0.16, 1.59, -0.43], [0.03, -0.44, 1.41]])),
    Camera("Canon R5", "ITU-R BT.709", np.array([[2.06, -1.22, 0.16], [-0.18, 1.57, -0.39], [0.06,  -0.62, 1.55]])),
    Camera("Sony A7R V", "ITU-R BT.709", np.array([[1.95, -0.87, -0.08], [-0.15, 1.58, -0.43], [0.03, -0.45, 1.41]])),
]

CAMERA_SPACES = []

for cam in CAMERA_MATRICES:
    if cam.storage == None:
        npm = cam.matrix
    else:
        storage_npm = colour.RGB_COLOURSPACES[cam.storage].matrix_RGB_to_XYZ
        npm = np.matmul(storage_npm, cam.matrix)

    primaries, whitepoint = colour.primaries_whitepoint(npm)
    space = colour.RGB_Colourspace(cam.name, primaries, whitepoint)
    CAMERA_SPACES.append(space)

whitepoint = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["D65"]
dignat_primaries = [
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
]

dists = [0.0, 0.0, 0.0]

for space in CAMERA_SPACES:
    for i in range(0, 3):
        dist = np.linalg.norm(space.primaries[i] - whitepoint)
        if dist > dists[i]:
            dignat_primaries[i] = space.primaries[i]
            dists[i] = dist

dignat = colour.RGB_Colourspace("Digital Native", dignat_primaries, whitepoint)
dignat.use_derived_transformation_matrices()

print("Digital Native to XYZ:\n", dignat.matrix_RGB_to_XYZ)
print("XYZ to Digital Native:\n", dignat.matrix_XYZ_to_RGB)

plot_ref = [
    "Alexa Wide Gamut",
    # "ITU-R BT.709",
]

colour.plotting.plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(CAMERA_SPACES + [dignat] + plot_ref)
