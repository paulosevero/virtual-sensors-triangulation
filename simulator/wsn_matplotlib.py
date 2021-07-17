# External libraries
import matplotlib.pyplot as plt

# Physical sensors
plt.scatter(1, 4, s=200, c='#333333')
plt.scatter(0, 0, s=200, c='#333333')
plt.scatter(2, 2, s=200, c='#333333')

# Logical sensor
plt.scatter(0.8, 1.5, s=200, c='#ff0000')


# Lines between physical sensors
x_values = [1, 0]
y_values = [4, 0]
plt.plot(x_values, y_values, c='#333333')

x_values = [0, 2]
y_values = [0, 2]
plt.plot(x_values, y_values, c='#333333')

x_values = [1, 2]
y_values = [4, 2]
plt.plot(x_values, y_values, c='#333333')


intersec_line1 = ((0, 0), (0.8, 1.5))
intersec_line2 = ((1, 4), (0.8, 1.5))
intersec_line3 = ((2, 2), (0.8, 1.5))
plt.axline(intersec_line1[0], intersec_line1[1], color='C3', label='by points')
plt.axline(intersec_line2[0], intersec_line2[1], color='C3', label='by points')
plt.axline(intersec_line3[0], intersec_line3[1], color='C3', label='by points')


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False




intersection1 = intersection(line([0, 0], [0.8, 1.5]), line([1, 4], [2, 2]))
plt.scatter(intersection1[0], intersection1[1], s=200, c='#008000')

intersection2 = intersection(line([1, 4], [0.8, 1.5]), line([0, 0], [2, 2]))
plt.scatter(intersection2[0], intersection2[1], s=200, c='#008000')

intersection3 = intersection(line([2, 2], [0.8, 1.5]), line([0, 0], [1, 4]))
plt.scatter(intersection3[0], intersection3[1], s=200, c='#008000')

print(f'intersection1 = {intersection1}')
print(f'intersection2 = {intersection2}')
print(f'intersection3 = {intersection3}')


plt.show()
