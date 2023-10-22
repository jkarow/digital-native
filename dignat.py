import colour
import matplotlib.pyplot as plt
import numpy as np

DIGNAT_WHITEPOINT = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["D65"]
PRECISION = 8
PLOT_REF = [
    # "Alexa Wide Gamut",
    # "ITU-R BT.709",
]
DARK_PLOT = True

class Camera:
    def __init__(cam, name, target, matrix):
        cam.name = name
        cam.target = target
        cam.matrix = matrix

# Sensor native to target matrices.
# Currently problematic:
# - Sony A7SIII
# - Sony A7C
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
    Camera("Sony A7C", "ITU-R BT.709", np.array([[1.9, -0.73, -0.17], [-0.17, 1.46, -0.29], [0.13, -0.8, 1.67]])),
    Camera("Sony A7R V", "ITU-R BT.709", np.array([[1.95, -0.87, -0.08], [-0.15, 1.58, -0.43], [0.03, -0.45, 1.41]])),
    Camera("Sony A7SIII", "ITU-R BT.709", np.array([[1.9, -0.71, -0.19], [-0.17, 1.47, -0.3], [0.13, -0.85, 1.72]])),
]

def space_from_camera_matrix(cam):
    if cam.target == None:
        npm = cam.matrix
    else:
        target_npm = colour.RGB_COLOURSPACES[cam.target].matrix_RGB_to_XYZ
        npm = np.matmul(target_npm, cam.matrix)

    primaries, whitepoint = colour.primaries_whitepoint(npm)
    return colour.RGB_Colourspace(cam.name, primaries, whitepoint)

def space_from_farthest_primaries(spaces, whitepoint, name):
    primaries = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
    dists = [0.0, 0.0, 0.0]

    for space in spaces:
        for i in range(0, 3):
            dist = np.linalg.norm(space.primaries[i] - whitepoint)
            if dist > dists[i]:
                primaries[i] = space.primaries[i]
                dists[i] = dist
    return colour.RGB_Colourspace(name, primaries, whitepoint)

def space_from_average_primaries(spaces, whitepoint, name):
    sum = np.zeros((3, 2))

    for space in spaces:
        sum += space.primaries

    primaries = sum / len(spaces)

    return colour.RGB_Colourspace(name, primaries, whitepoint)

def format_matrix_plaintext(mat, precision = 8):
    mat = np.round(mat, precision)
    return f"""\
{mat[0][0]} {mat[0][1]} {mat[0][2]}
{mat[1][0]} {mat[1][1]} {mat[1][2]}
{mat[2][0]} {mat[2][1]} {mat[2][2]}"""

def main():
    camera_spaces = []
    for camera in CAMERA_MATRICES:
        camera_spaces.append(space_from_camera_matrix(camera))

    dignat = space_from_average_primaries(camera_spaces, DIGNAT_WHITEPOINT, "Digital Native")
    dignat.use_derived_transformation_matrices()

    print("Digital Native to XYZ:")
    print(format_matrix_plaintext(dignat.matrix_RGB_to_XYZ, PRECISION))
    print("XYZ to Digital Native:")
    print(format_matrix_plaintext(dignat.matrix_XYZ_to_RGB, PRECISION))

    if DARK_PLOT:
        plt.style.use("dark_background")

    figure, axes = colour.plotting.plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(
        camera_spaces + [dignat] + PLOT_REF,
        standalone = False
    )
    axes.legend(bbox_to_anchor=(1.02, 1.01))
    plt.title("Digital Native Comparison")
    plt.show()

main()
