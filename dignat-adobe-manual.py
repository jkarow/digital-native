import colour
import matplotlib.pyplot as plt
import numpy as np
import os

PRECISION = 8
DARK_PLOT = False

def format_matrix_plaintext(mat, precision = 8):
    mat = np.round(mat, precision)
    return f"""\
{mat[0][0]} {mat[0][1]} {mat[0][2]}
{mat[1][0]} {mat[1][1]} {mat[1][2]}
{mat[2][0]} {mat[2][1]} {mat[2][2]}"""

# Adobe ColorMatrix2 to usable camera matrix "NPM".
def cm2_to_camera_matrix(input):
    # ColorMatrix2 is XYZ to camera native.
    colormatrix2 = np.asarray(input, dtype=float)
    colormatrix2 /= 10_000

    bt709_to_xyz = colour.RGB_COLOURSPACES["ITU-R BT.709"].matrix_RGB_to_XYZ

    bt709_to_camnat = np.matmul(colormatrix2, bt709_to_xyz)

    # Scale so all rows sum to one. This does not change ratios
    # between each coefficient; only scales all three. The key and
    # weird bit is that it's on BT.709.
    bt709_to_camnat[0] = bt709_to_camnat[0] / np.sum(bt709_to_camnat[0])
    bt709_to_camnat[1] = bt709_to_camnat[1] / np.sum(bt709_to_camnat[1])
    bt709_to_camnat[2] = bt709_to_camnat[2] / np.sum(bt709_to_camnat[2])

    # Comparable to DXOMark matrices.
    camnat_to_bt709 = np.linalg.inv(bt709_to_camnat)
    return np.matmul(bt709_to_xyz, camnat_to_bt709)

color_matrix_txt = os.listdir("adobe-matrices")

cam_red_primaries = np.zeros((len(color_matrix_txt), 2))
cam_grn_primaries = np.zeros((len(color_matrix_txt), 2))
cam_blu_primaries = np.zeros((len(color_matrix_txt), 2))

for i, file in enumerate(color_matrix_txt):
    raw_matrix = np.loadtxt(f"adobe-matrices/{file}", delimiter=',')
    cam_matrix = cm2_to_camera_matrix(raw_matrix)
    primaries, _ = colour.primaries_whitepoint(cam_matrix)
    cam_red_primaries[i] = primaries[0]
    cam_grn_primaries[i] = primaries[1]
    cam_blu_primaries[i] = primaries[2]

del color_matrix_txt

dignat_primaries = np.array([
    [0.948, 0.186],
    [0.124, 1.785],
    [-0.041, -0.305],
])
dignat_whitepoint = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["D65"]
dignat = colour.RGB_Colourspace("Digital Native", dignat_primaries, dignat_whitepoint)
dignat.use_derived_transformation_matrices()

print("Digital Native to XYZ:")
print(format_matrix_plaintext(dignat.matrix_RGB_to_XYZ, PRECISION))
print("XYZ to Digital Native:")
print(format_matrix_plaintext(dignat.matrix_XYZ_to_RGB, PRECISION))

if DARK_PLOT:
    plt.style.use("dark_background")

colour.plotting.plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(dignat, show = True)
plt.scatter(cam_red_primaries[:, 0], cam_red_primaries[:, 1], color="red")
plt.scatter(cam_grn_primaries[:, 0], cam_grn_primaries[:, 1], color="green")
plt.scatter(cam_blu_primaries[:, 0], cam_blu_primaries[:, 1], color="blue")
plt.show()
