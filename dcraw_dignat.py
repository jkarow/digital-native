import colour
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("dark_background")

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


flattened = np.loadtxt("dcraw_cameras.txt", delimiter=",")
camera_primaries = np.array([np.zeros((3, 2))] * len(flattened))

for i in range(len(flattened)):
    # 1x9 in.
    cm2_matrix = np.reshape(flattened[i], (3, 3))
    camera_matrix = cm2_to_camera_matrix(cm2_matrix)
    primaries, _ = colour.primaries_whitepoint(camera_matrix)
    camera_primaries[i] = primaries

del flattened

colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False)

xp = camera_primaries[:, :, 0].flatten()
yp = camera_primaries[:, :, 1].flatten()

plt.scatter(xp, yp)
plt.show()
