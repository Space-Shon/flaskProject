from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/save_and_process_temperature', methods=['POST'])
def save_and_process_temperature():
    data = request.json
    temperature = data.get('temperature')

    with open('input_for_cpp.txt', 'w') as file:
        file.write(str(temperature))

    cntTemperature()

    with open('output_from_python.txt', 'r') as file:
        result = file.read().strip()

    return jsonify({"message": result})


if __name__ == '__main__':
    app.run(debug=True)


def f1(x, y):
    return 0.0


def f2(x):
    return 1.0


def init(a, b, c, h):
    Nx = int((b - a) / h)
    Ny = int((b - c) / h)
    u = np.zeros((Nx + 1, Ny + 1))

    for i in range(Nx + 1):
        x = a + i * h
        for j in range(Ny + 1):
            y = c + j * h
            u[i][j] = f1(x, y)

    for j in range(Ny + 1):
        y = c + j * h
        u[0][j] = f2(y)
        u[Nx][j] = f2(y)

    for i in range(Nx + 1):
        x = a + i * h
        u[i][0] = f2(x)
        u[i][Ny] = f2(x)

    return u


def read_temperature():
    try:
        with open('input_for_cpp.txt', 'r') as file:
            temperature = float(file.read().strip())
            return temperature
    except Exception as e:
        print(f"Error reading temperature file: {e}")
        return None


def cntTemperature():
    temperature = read_temperature()

    if temperature is None:
        return

    a, b, c = 0.0, 15.0, 0.0
    h = 0.5
    tau = 0.01
    Nx = int((b - a) / h)
    Ny = int((b - c) / h)

    u = init(a, b, c, h)
    prev_u = np.copy(u)

    t = 0.0

    with open("output_from_python.txt", "w") as explicit_file:
        explicit_file.write(f"t = {t}\n")
        for i in range(Nx + 1):
            explicit_file.write(" ".join(map(str, u[i])) + "\n")

        if 30 <= temperature <= 55:
            D = 0.0586 * temperature - 0.7558
        elif 55 < temperature <= 74:
            D = 0.0510 * temperature - 0.3400
        elif 74 < temperature <= 85:
            D = 0.0924 * temperature - 3.4009
        elif 85 < temperature <= 94:
            D = 0.1556 * temperature - 8.7722
        else:
            print("Temperature out of range")
            return

        stop = False
        while not stop:
            prev_u = np.copy(u)
            for i in range(1, Nx):
                for j in range(1, Ny):
                    u[i][j] = (D * ((prev_u[i + 1][j] - 2 * prev_u[i][j] + prev_u[i - 1][j]) / (h * h) +
                                    (prev_u[i][j + 1] - 2 * prev_u[i][j] + prev_u[i][j - 1]) / (h * h)) * tau +
                               prev_u[i][j])
                    if (u[i][j] > 1) or (u[i][j] + 0.001) >= 1:
                        u[i][j] = 1

            center = int((b - a) / h / 2)
            if u[center][center] == 1:
                stop = True

            t += tau
            explicit_file.write(f"t = {t}\n")
            for i in range(Nx + 1):
                explicit_file.write(" ".join(map(str, u[i])) + "\n")

    print(t)
