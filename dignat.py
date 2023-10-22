import colour
import matplotlib.pyplot as plt
import numpy as np

# plt.style.use("dark_background")

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
    Camera("Canon EOS R3", "ITU-R BT.709", np.array([[2.02, -1.15, 0.14], [-0.17, 1.52, -0.36], [0.05, -0.55, 1.5]])),
    Camera("Canon EOS R5", "ITU-R BT.709", np.array([[2.06, -1.22, 0.16], [-0.18, 1.57, -0.39], [0.06,  -0.62, 1.55]])),
    Camera("Hasselblad X1D-50c", "ITU-R BT.709", np.array([[2.13, -0.98, -0.14], [-0.15, 1.55, -0.39], [0.03, -0.44, 1.41]])),
    Camera("Leica M11", "ITU-R BT.709", np.array([[1.9, -0.93, 0.03], [-0.15, 1.5, -0.35], [ 0.03, -0.53, 1.5]])),
    Camera("Leica Q2", "ITU-R BT.709", np.array([[1.6, -0.47, -0.13], [-0.09, 1.19, -0.1], [0.04, -0.34, 1.3]])),
    Camera("Nikon Z7II", "ITU-R BT.709", np.array([[1.81, -0.72, -0.09], [-0.14, 1.44, -0.31], [0.03, -0.46, 1.43]])),
    Camera("Olympus OM-D E-M1 Mark II", "ITU-R BT.709", np.array([[2.04, -0.97, -0.07], [-0.23, 1.59, -0.36], [0.11, -0.66, 1.55]])),
    Camera("Panasonic Lumix DC-S1R", "ITU-R BT.709", np.array([[1.61, -0.52, -0.09], [-0.08, 1.15, -0.07], [ 0.05, -0.4,  1.35]])),
    Camera("Pentax 645Z", "ITU-R BT.709", np.array([[1.87, -0.81, -0.06], [-0.16, 1.56, -0.4], [0.09, -0.59, 1.5]])),
    Camera("Sony A7", "ITU-R BT.709", np.array([[1.93, -0.79, -0.14], [-0.16, 1.59, -0.43], [0.03, -0.44, 1.41]])),
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

dignat_whitepoint = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["D65"]
dignat_primaries = [
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
]

dists = [0.0, 0.0, 0.0]

for space in CAMERA_SPACES:
    for i in range(0, 3):
        dist = np.linalg.norm(space.primaries[i] - dignat_whitepoint)
        if dist > dists[i]:
            dignat_primaries[i] = space.primaries[i]
            dists[i] = dist

dignat = colour.RGB_Colourspace("Digital Native", dignat_primaries, dignat_whitepoint)
dignat.use_derived_transformation_matrices()

print("Digital Native to XYZ:\n", dignat.matrix_RGB_to_XYZ)
print("XYZ to Digital Native:\n", dignat.matrix_XYZ_to_RGB)

plot_ref = [
    "Alexa Wide Gamut",
    # "ITU-R BT.709",
]

figure, axes = colour.plotting.plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(CAMERA_SPACES + [dignat] + plot_ref)
axes.legend(bbox_to_anchor=(1.02, 1.01))
plt.title("Digital Native Comparison")
plt.show()
