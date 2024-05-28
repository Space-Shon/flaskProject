#define _USE_MATH_DEFINES
#include <iostream>
#include <fstream>
#include <cmath>
#include <algorithm>

using namespace std;

double f1(double x, double y) {
    return 0.0;
}

double f2(double y) {
    return 1.0;
}


double** init(double a, double b, double c, double h) {
    int Nx = static_cast<int>((b - a) / h);
    int Ny = static_cast<int>((b - c) / h);

    double** u = new double* [Nx + 1];
    for (int i = 0; i <= Nx; ++i) {
        double x = a + i * h;
        u[i] = new double[Ny + 1];
        for (int j = 0; j <= Ny; ++j) {
            double y = c + j * h;
            u[i][j] = f1(x, y);
        }
    }

    for (int j = 0; j <= Ny; ++j) {
        double y = c + j * h;
        u[0][j] = f2(y);
        u[Nx][j] = f2(y);
    }

    for (int i = 0; i <= Nx; ++i) {
        double x = a + i * h;
        u[i][0] = f2(x);
        u[i][Ny] = f2(x);
    }

    return u;
}


int main() {
    double a = 0.0, b = 15.0, c = 0.0;
    double h = 0.5;
    double tau = 0.01, temperature = 94; 
    int Nx = static_cast<int>((b - a) / h);
    int Ny = static_cast<int>((b - c) / h);

    double** u = init(a, b, c, h);
    double** prev_u = new double* [Nx + 1];

    double t = 0.0;

    for (int i = 0; i <= Nx; ++i) {
        prev_u[i] = new double[Ny + 1];
    }

    ofstream explicit_file("output_from_cpp.txt");
    explicit_file << "t = " << t << endl;
    for (int i = 0; i <= Nx; i++) {
        for (int j = 0; j <= Ny; j++) {
            explicit_file << u[i][j] << " ";
        }
        explicit_file << endl;
    }
    explicit_file;
    double D;
    bool stop = false;
    int count;
    if (temperature >= 30 && temperature <= 55) {
        D = 0.0586 * temperature - 0.7558;
    }
    else if (temperature > 55 && temperature <= 74) {
        D = 0.0510 * temperature - 0.3400;
    }
    else if (temperature > 74 && temperature <= 85) {
        D = 0.0924 * temperature - 3.4009;
    }
    else if (temperature > 85 && temperature <= 94) {
        D = 0.1556 * temperature - 8.7722;
    }
    else {
        cout << "Temperature out of range\n";
        exit(0);
    }
    while (!stop) {
        count = 0;
        for (int i = 0; i <= Nx; i++) {
            for (int j = 0; j <= Ny; j++) {
                prev_u[i][j] = u[i][j];
            }
        }
        for (int i = 1; i < Nx; i++) {
            for (int j = 1; j < Ny; j++) {
                u[i][j] = D * ((prev_u[i + 1][j] - 2 * prev_u[i][j] + prev_u[i - 1][j]) / (h * h) * tau + (prev_u[i][j + 1] - 2 * prev_u[i][j] + prev_u[i][j - 1]) / (h * h)) * tau + prev_u[i][j];

                if ((u[i][j] > 1) || (u[i][j] + 0.001) >= 1) u[i][j] = 1;
            }
        }
        int center = (b - a) / h / 2;
        if (u[center][center] == 1) stop = true;
        t += tau;
        explicit_file << "t = " << t << endl;
        for (int i = 0; i <= Nx; i++) {
            for (int j = 0; j <= Ny; j++) {
                explicit_file << u[i][j] << " ";
            }
            explicit_file << endl;
        }
        explicit_file;
    }
    std::cout << t << endl;
    explicit_file.close();
    return 0;
}