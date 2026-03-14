#include <iostream>
#include <cmath>
#include <vector>
#include <fstream>
#include <chrono>
#include <random>
#include <iomanip>

const double PI = 3.14159265358979323846;

// Definicje badanych funkcji i ich wartosci analityczne
double f1(double x) { 
    return -x * x + 4.0 * x; 
}
const double a1 = 0.0, b1 = 4.0, y_max1 = 4.0;
const double exact_f1 = 32.0 / 3.0;

double f2(double x) { 
    return std::exp(-x) * std::sin(4.0 * PI * x) + 2.0; 
}
const double a2 = 0.0, b2 = 2.0, y_max2 = 3.0; 
const double exact_f2 = 4.0 + (4.0 * PI * (1.0 - std::exp(-2.0))) / (1.0 + 16.0 * PI * PI);

typedef double (*FunctionPtr)(double);

// Algorytmy calkowania

double rect_left(FunctionPtr f, double a, double b, int n) {
    double dx = (b - a) / n;
    double sum = 0.0;
    for (int i = 0; i < n; ++i) sum += f(a + i * dx);
    return sum * dx;
}

double rect_right(FunctionPtr f, double a, double b, int n) {
    double dx = (b - a) / n;
    double sum = 0.0;
    for (int i = 1; i <= n; ++i) sum += f(a + i * dx);
    return sum * dx;
}

double rect_mid(FunctionPtr f, double a, double b, int n) {
    double dx = (b - a) / n;
    double sum = 0.0;
    for (int i = 0; i < n; ++i) sum += f(a + (i + 0.5) * dx);
    return sum * dx;
}

double trapezoid(FunctionPtr f, double a, double b, int n) {
    double dx = (b - a) / n;
    double sum = (f(a) + f(b)) / 2.0;
    for (int i = 1; i < n; ++i) sum += f(a + i * dx);
    return sum * dx;
}

double monte_carlo(FunctionPtr f, double a, double b, double y_max, int n) {
    int hits = 0;
    std::mt19937 gen(1337); // mt19937 zamiast rand() dla lepszego rozkladu punktow 
    std::uniform_real_distribution<double> dist_x(a, b);
    std::uniform_real_distribution<double> dist_y(0.0, y_max);

    for (int i = 0; i < n; ++i) {
        if (dist_y(gen) <= f(dist_x(gen))) {
            hits++;
        }
    }
    return (b - a) * y_max * ((double)hits / n);
}

// Zapis wynikow

void run_experiments(FunctionPtr f, double a, double b, double y_max, double exact_val, const std::string& filename) {
    std::ofstream file(filename);
    file << "N,Method,Result,Expected,AbsError,Time_ns\n";
    
    std::vector<int> n_values = {10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000};
    std::vector<std::string> methods = {"RectLeft", "RectRight", "RectMid", "Trapezoid", "MonteCarlo"};

    for (int n : n_values) {
        for (const auto& method : methods) {
            double result = 0.0;
            auto start = std::chrono::high_resolution_clock::now();
            
            if (method == "RectLeft") result = rect_left(f, a, b, n);
            else if (method == "RectRight") result = rect_right(f, a, b, n);
            else if (method == "RectMid") result = rect_mid(f, a, b, n);
            else if (method == "Trapezoid") result = trapezoid(f, a, b, n);
            else if (method == "MonteCarlo") result = monte_carlo(f, a, b, y_max, n);
            
            auto end = std::chrono::high_resolution_clock::now();
            long long time_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
            
            double abs_error = std::abs(result - exact_val);
            
            file << std::fixed << std::setprecision(10) 
                 << n << "," << method << "," << result << "," << exact_val << "," 
                 << abs_error << "," << time_ns << "\n";
        }
    }
    file.close();
}

int main() {
    run_experiments(f1, a1, b1, y_max1, exact_f1, "wyniki_f1.csv");
    run_experiments(f2, a2, b2, y_max2, exact_f2, "wyniki_f2.csv");
    return 0;
}