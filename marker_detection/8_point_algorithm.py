import numpy as np
import cv2


def compute_essential_matrix(p1, p2, return_sigma=False):
    """
    This function compute the Essential matrix of a pair of Nx3 points. The points must be matched each other
    from two geometry views (Epipolar constraint). This general function doesn't assume a homogeneous
    representation of points.
    :param p1: Points from the 1st frame (n, 3) [u, v, 1]
    :param p2: Points from the 2st frame (n, 3) [u, v, 1]
    :return: Essential Matrix (3,3)
    """

    assert p1.shape == p2.shape, f"Shapes do not match {p1.shape} != {p2.shape}"
    assert p1.shape[1] in [3, 4], f"PCL out of shape {p1.shape} != (3, n) or (4, n)"

    A = A_matrix(p1, p2)

    # ! compute linear least square solution
    U, Sigma, V = np.linalg.svd(A)  # svd singular value decomposition
    E = V[-1].reshape(3, 3)

    # ! constraint E
    # ! making E rank 2 by setting out the last singular value
    U, S, V = np.linalg.svd(E)
    S[2] = 0
    E = np.dot(U, np.dot(np.diag(S), V))
    if return_sigma:
        return E / np.linalg.norm(E), Sigma
    return E / np.linalg.norm(E)


def A_matrix(p1, p2):
    """
    Build an observation matrix A of the linear equation AX=0. This function doesn't assume
    homogeneous coordinates on a plane for p1s, and p2s
    :param p1:  Pixel coordinates from the 1st frame (n, 3) [u, v, 1]
    :param p2: Pixel coordinates from 2nd frame (n, 3) [u, v, 1]
    :return:  Matrix (n x 9)
    """

    A = np.array([
        [p1[0][0] * p2[0][0], p1[0][0] * p2[0][1], p1[0][0], p1[0][1] * p2[0][0], p1[0][1] * p2[0][1], p1[0][1],
         p2[0][0], p2[0][1], 1],
        [p1[1][0] * p2[1][0], p1[1][0] * p2[1][1], p1[1][0], p1[1][1] * p2[1][0], p1[1][1] * p2[1][1], p1[1][1],
         p2[1][0], p2[1][1], 1],
        [p1[2][0] * p2[2][0], p1[2][0] * p2[2][1], p1[2][0], p1[2][1] * p2[2][0], p1[2][1] * p2[2][1], p1[2][1],
         p2[2][0], p2[2][1], 1],
        [p1[3][0] * p2[3][0], p1[3][0] * p2[3][1], p1[3][0], p1[3][1] * p2[3][0], p1[3][1] * p2[3][1], p1[3][1],
         p2[3][0], p2[3][1], 1],
        [p1[4][0] * p2[4][0], p1[4][0] * p2[4][1], p1[4][0], p1[4][1] * p2[4][0], p1[4][1] * p2[4][1], p1[4][1],
         p2[4][0], p2[4][1], 1],
        [p1[5][0] * p2[5][0], p1[5][0] * p2[5][1], p1[5][0], p1[5][1] * p2[5][0], p1[5][1] * p2[5][1], p1[5][1],
         p2[5][0], p2[5][1], 1],
        [p1[6][0] * p2[6][0], p1[6][0] * p2[6][1], p1[6][0], p1[6][1] * p2[6][0], p1[6][1] * p2[6][1], p1[6][1],
         p2[6][0], p2[6][1], 1],
        [p1[7][0] * p2[7][0], p1[7][0] * p2[7][1], p1[7][0], p1[7][1] * p2[7][0], p1[7][1] * p2[7][1], p1[7][1],
         p2[7][0], p2[7][1], 1]]
    )

    return A


p1 = np.array([[1871, 363, 1],
               [175, 363, 1],
               [63, 343, 1],
               [1755, 376, 1],
               [1315, 376, 1],
               [1412, 351, 1],
               [1243, 376, 1],
               [803, 376, 1],
               ])

p2 = np.array([[1943, 382, 1],
               [255, 260, 1],
               [65, 289, 1],
               [1870, 408, 1],
               [1582, 429, 1],
               [1641, 417, 1],
               [1535, 428, 1],
               [1233, 389, 1],
               ])

Essential = compute_essential_matrix(p1, p2)
print(Essential)
R1, R2, t = cv2.decomposeEssentialMat(Essential)

print("R1:", R1, "\n\n", "R2:", R2, "\n\n", "t:", t, "\n")

np.set_printoptions(suppress=True)
print("R1:", R1)
print("\n")
print("t:", t)

print("\n")
for i in range(p2.shape[0]):
    validation = (p2[i].T @ Essential @ p1[i])

    print(f'{validation:f}')
