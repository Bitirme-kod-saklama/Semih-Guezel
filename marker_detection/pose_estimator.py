from pose_estimation.sonolsun import *

stickers = np.array([[1, 0, 0], [7, 0, 0], [9, 0, 0], [4, 0, 10], [8, 0, 10], [0, 0, 2], [0, 0, 4], [0, 0, 8]])

sticker_pixel = np.array([[1024.0, 540.0, 1],
                          [1482.2, 540.0, 1],
                          [1495.5, 540.0, 1],
                          [1943.1, 540.0, 1],
                          [1832.5, 540.0, 1],
                          [256.0, 540.0, 1],
                          [105.0, 540.0, 1],
                          [46.3, 540.0, 1],
                          ])

unit_stickers = stickers / np.linalg.norm(stickers)

print("unit sticker :", "\n", unit_stickers)
print("\n")

theta = 0  # rotation angle in rad

origin = np.array([[0, 0, 0]])
vehicle = np.array([3, 0, 8])

# # rotation in z axis
# R = np.array([[np.cos(theta), -np.sin(theta), 0],
#               [np.sin(theta), np.cos(theta), 0],
#               [0, 0, 1]])

# rotation in y axis
R = np.array([[np.cos(theta), 0, np.sin(theta)],
              [0, 1, 0],
              [-np.sin(theta), 0, np.cos(theta)]])

W = 2048
H = 1080
# This matrix were used to convert pixel coordinates to spherical coordinates
p2s_matrix = np.array([[(2 * np.pi) / W, 0, -np.pi],
                       [0, -np.pi / H, np.pi / 2]
                       ])
qN = np.zeros((8, 3))

for i in range(len(stickers)):
    pixel_array = np.array([[sticker_pixel[i][0]],
                            [sticker_pixel[i][1]],
                            [sticker_pixel[i][2]]])
    spherical_angles = np.matmul(p2s_matrix, pixel_array)

    az = spherical_angles[0][0]
    el = spherical_angles[1][0]

    qN[i] = (np.array([[np.cos(el) * np.sin(az)],
                       [-np.sin(el)],
                       [np.cos(el) * np.cos(az)]])).T

print("qN :", "\n", qN)
print("\n")


E = compute_essential_matrix(unit_stickers, qN)
print("Essential Matrix :", "\n", E)
print("\n")

rec_pose = recover_pose_from_e(E, unit_stickers.T, qN.T)
print("recover pose :", "\n", rec_pose)
print("\n")

R1, R2, t = cv2.decomposeEssentialMat(E)

print("R1:", R1, "\n\n", "R2:", R2, "\n\n", "t:", t, "\n")

for i in range(qN.shape[0]):
    validation = (qN[i].T @ E @ unit_stickers[i])
    print(validation)
