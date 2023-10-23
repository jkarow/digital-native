import colour
import matplotlib.pyplot as plt
import numpy as np

DIGNAT_WHITEPOINT = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["D65"]
PRECISION = 8
DARK_PLOT = False
PLOT_REF = [
    # "Alexa Wide Gamut",
    # "ITU-R BT.709",
]

class Camera:
    def __init__(cam, name, target, matrix):
        cam.name = name
        cam.target = target
        cam.matrix = matrix

# Sensor native to target matrices.
# Currently problematic:
# - Sony A7SIII
# - Sony A7C
# This must be due to R-G filter overlap.
CAMERA_MATRICES = [
    Camera("ARRI Alexa", "Alexa Wide Gamut", np.array([[1.16568936, -0.18400079, 0.01831143], [-0.0524356, 1.01472615, 0.03770945], [0.0270692, -0.24782896, 1.22075976]])),
    Camera("Canon EOS R3", "ITU-R BT.709", np.array([[2.02, -1.15, 0.14], [-0.17, 1.52, -0.36], [0.05, -0.55, 1.5]])),
    Camera("Canon EOS R5", "ITU-R BT.709", np.array([[2.06, -1.22, 0.16], [-0.18, 1.57, -0.39], [0.06,  -0.62, 1.55]])),
    Camera("Canon EOS R6", "ITU-R BT.709", np.array([[2.12, -1.24, 0.12], [-0.21, 1.7, -0.49], [0.04, -0.65, 1.61]])),
    Camera("Hasselblad X1D-50c", "ITU-R BT.709", np.array([[2.13, -0.98, -0.14], [-0.15, 1.55, -0.39], [0.03, -0.44, 1.41]])),
    Camera("Leica M11", "ITU-R BT.709", np.array([[1.9, -0.93, 0.03], [-0.15, 1.5, -0.35], [ 0.03, -0.53, 1.5]])),
    Camera("Leica Q2", "ITU-R BT.709", np.array([[1.6, -0.47, -0.13], [-0.09, 1.19, -0.1], [0.04, -0.34, 1.3]])),
    Camera("Nikon Z7II", "ITU-R BT.709", np.array([[1.81, -0.72, -0.09], [-0.14, 1.44, -0.31], [0.03, -0.46, 1.43]])),
    Camera("Nikon Z9", "ITU-R BT.709", np.array([[1.74, -0.64, -0.1], [-0.13, 1.43, -0.3], [0.02, -0.43, 1.41]])),
    Camera("Olympus OM-D E-M1 Mark II", "ITU-R BT.709", np.array([[2.04, -0.97, -0.07], [-0.23, 1.59, -0.36], [0.11, -0.66, 1.55]])),
    Camera("Panasonic Lumix DC-GH5 II", "ITU-R BT.709", np.array([[2.01, -0.96, -0.05], [-0.23, 1.61, -0.39], [0.1, -0.71, 1.61]])),
    Camera("Panasonic Lumix DC-S1R", "ITU-R BT.709", np.array([[1.61, -0.52, -0.09], [-0.08, 1.15, -0.07], [ 0.05, -0.4,  1.35]])),
    Camera("Panasonic Lumix DC-S5", "ITU-R BT.709", np.array([[1.94, -0.85, -0.09], [-0.17, 1.55, -0.38], [0.07, -0.63, 1.56]])),
    Camera("Pentax 645Z", "ITU-R BT.709", np.array([[1.87, -0.81, -0.06], [-0.16, 1.56, -0.4], [0.09, -0.59, 1.5]])),
    Camera("Pentax K-1", "ITU-R BT.709", np.array([[1.8, -0.67, -0.13], [-0.15, 1.54, -0.39], [0.07, -0.47, 1.4]])),
    Camera("Phase One P65 Plus", "ITU-R BT.709", np.array([[2.52, -1.56, 0.04], [-0.3, 1.84, -0.54], [-0.14, -0.41, 1.55]])),


    # "REDWideGamutRGB (RWG) is a camera color space designed to encompass all colors a RED camera can
    #  generate without clipping. Essentially RWG is a standardized CameraRGB color space."
    # https://s3.amazonaws.com/red_3/downloads/other/white-papers/REDWIDEGAMUTRGB%20AND%20LOG3G10%20Rev-B.pdf
    # This works and is good for comparison, however the artificial red primary is rotated exceptionally far,
    # hence why it's not used.
    # Camera("RED Generic", None, np.array([[0.735275, 0.068609, 0.146571], [0.286694, 0.842979, -0.129673], [-0.079681, -0.347343, 1.516082]])),

    Camera("Sony A7", "ITU-R BT.709", np.array([[1.93, -0.79, -0.14], [-0.16, 1.59, -0.43], [0.03, -0.44, 1.41]])),
    # Camera("Sony A7C", "ITU-R BT.709", np.array([[1.9, -0.73, -0.17], [-0.17, 1.46, -0.29], [0.13, -0.8, 1.67]])),
    Camera("Sony A7R V", "ITU-R BT.709", np.array([[1.95, -0.87, -0.08], [-0.15, 1.58, -0.43], [0.03, -0.45, 1.41]])),
    Camera("Sony A7R III", "ITU-R BT.709", np.array([[2.01, -0.91, -0.11], [-0.18, 1.57, -0.39], [0.04, -0.52, 1.48]])),
    Camera("Sony A7S", "ITU-R BT.709", np.array([[2.29, -1.1, -0.2], [-0.25, 1.71, -0.46], [0.12, -0.7, 1.58]])),
    # Camera("Sony A7S III", "ITU-R BT.709", np.array([[1.9, -0.71, -0.19], [-0.17, 1.47, -0.3], [0.13, -0.85, 1.72]])),
]

def make_vec(length):
    return [None] * length

def derive_camera_space(cam):
    if cam.target == None:
        npm = cam.matrix
    else:
        target_npm = colour.RGB_COLOURSPACES[cam.target].matrix_RGB_to_XYZ
        npm = np.matmul(target_npm, cam.matrix)

    primaries, whitepoint = colour.primaries_whitepoint(npm)
    return colour.RGB_Colourspace(cam.name, primaries, whitepoint)

def farthest_primaries(spaces, whitepoint, name):
    primaries = np.zeros((3, 2))
    dists = np.zeros(3)

    for space in spaces:
        for i in range(0, 3):
            dist = np.linalg.norm(space.primaries[i] - whitepoint)
            if dist > dists[i]:
                primaries[i] = space.primaries[i]
                dists[i] = dist
    return colour.RGB_Colourspace(name, primaries, whitepoint)

def average_primaries(spaces, whitepoint, name):
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
    camera_spaces = make_vec(len(CAMERA_MATRICES))
    for i in range(0, len(CAMERA_MATRICES)):
        camera_spaces[i] = derive_camera_space(CAMERA_MATRICES[i])

    dignat = farthest_primaries(camera_spaces, DIGNAT_WHITEPOINT, "Digital Native")
    dignat.use_derived_transformation_matrices()

    print("Digital Native primaries:")
    print(dignat.primaries)

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
