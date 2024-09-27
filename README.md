# A* Search Algorithm

Implementation of the A* Search Algorithm in Python. We use a 8x8 chess board with the following conditions:
* White is given a rook and king (both can move freely)
  * Rook is in the position (7, 0) (bottom right)
  * King is in the position (7, 4) (near the center of the bottom row of the board)
* Black is only given the king (not allowed to move)
  * King is in the position (0, 4) (facing the white king on the first row)

The objective is to find the most ideal set of movements to checkmate the black king.
