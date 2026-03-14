import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def f1(x):
    return -x**2 + 4*x

def f2(x):
    return np.exp(-x) * np.sin(4 * np.pi * x) + 2

def plot_method_shapes(f, a, b, y_max, N, title_prefix):
    x_fine = np.linspace(a, b, 1000)
    y_fine = f(x_fine)
    dx = (b - a) / N
    x_edges = np.linspace(a, b, N + 1)
    
    fig, axs = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle(f'Wizualizacja metod dla {title_prefix} (N={N})', fontsize=16, fontweight='bold')
    axs = axs.flatten()

    for ax in axs[:5]:
        ax.plot(x_fine, y_fine, 'k-', linewidth=2, label='f(x)')
        ax.set_xlim(a - 0.1, b + 0.1)
        ax.set_ylim(0, y_max + 0.5)
        ax.grid(True, linestyle='--', alpha=0.6)

    axs[0].bar(x_edges[:-1], f(x_edges[:-1]), width=dx, align='edge', alpha=0.4, color='blue', edgecolor='black')
    axs[0].set_title('Prostokąty (Lewe)')

    axs[1].bar(x_edges[1:] - dx, f(x_edges[1:]), width=dx, align='edge', alpha=0.4, color='green', edgecolor='black')
    axs[1].set_title('Prostokąty (Prawe)')

    x_mid = x_edges[:-1] + dx / 2
    axs[2].bar(x_mid - dx/2, f(x_mid), width=dx, align='edge', alpha=0.4, color='orange', edgecolor='black')
    axs[2].set_title('Prostokąty (Środek)')

    axs[3].fill_between(x_edges, 0, f(x_edges), alpha=0.4, color='purple', edgecolor='black')
    axs[3].plot(x_edges, f(x_edges), 'ro', markersize=4)
    axs[3].set_title('Trapezy')

    np.random.seed(42)
    N_mc = N * 10
    pts_x = np.random.uniform(a, b, N_mc)
    pts_y = np.random.uniform(0, y_max, N_mc)
    under_curve = pts_y <= f(pts_x)
    
    axs[4].plot([a, b, b, a, a], [0, 0, y_max, y_max, 0], 'r--', linewidth=2, label='Obszar losowania')
    axs[4].scatter(pts_x[under_curve], pts_y[under_curve], color='green', s=15, label='Trafione')
    axs[4].scatter(pts_x[~under_curve], pts_y[~under_curve], color='red', s=15, label='Chybione')
    axs[4].set_title(f'Monte Carlo (pokazowo {N_mc} pkt)')
    axs[4].legend(loc='upper right', fontsize='small')

    axs[5].axis('off')
    plt.tight_layout()
    plt.show()

def analyze_data():
    try:
        df1 = pd.read_csv('wyniki_f1.csv')
        df2 = pd.read_csv('wyniki_f2.csv')
    except FileNotFoundError:
        print("Brak plikow CSV. Uruchom najpierw program w C++.")
        return

    plt.figure(figsize=(10, 6))
    for method in df1['Method'].unique():
        data = df1[df1['Method'] == method]
        plt.loglog(data['N'], data['AbsError'], marker='o', label=method)
    
    plt.title('Funkcja Prosta (f1) - Błąd bezwzględny vs N')
    plt.xlabel('N (skala log)')
    plt.ylabel('Błąd bezwzględny (skala log)')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.show()

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Analiza funkcji skomplikowanej (f2)', fontsize=14, fontweight='bold')

    for method in df2['Method'].unique():
        data = df2[df2['Method'] == method]
        axs[0].loglog(data['N'], data['AbsError'], marker='.', label=method)
    axs[0].set_title('Błąd bezwzględny vs N')
    axs[0].set_xlabel('N')
    axs[0].set_ylabel('Błąd')
    axs[0].grid(True, which="both", ls="--")
    axs[0].legend()

    exact_val2 = df2['Expected'].iloc[0]
    axs[1].axhline(y=exact_val2, color='r', linestyle='--', linewidth=2, label='Wartość analityczna')
    for method in ['RectMid', 'MonteCarlo']:
        data = df2[df2['Method'] == method]
        axs[1].plot(data[data['N']<=500]['N'], data[data['N']<=500]['Result'], marker='x', label=method)
    axs[1].set_title('Zbieżność (małe N)')
    axs[1].set_xlabel('N')
    axs[1].set_ylabel('Wartość całki')
    axs[1].grid(True)
    axs[1].legend()

    for method in df2['Method'].unique():
        data = df2[df2['Method'] == method]
        axs[2].plot(data['N'], data['Time_ns'], marker='.', label=method)
    axs[2].set_title('Czas obliczeń vs N')
    axs[2].set_xlabel('N')
    axs[2].set_ylabel('Czas [ns]')
    axs[2].set_xscale('log')
    axs[2].set_yscale('log')
    axs[2].grid(True, which="both", ls="--")
    axs[2].legend()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    plot_method_shapes(f1, 0, 4, 4, 5, "f1")
    plot_method_shapes(f2, 0, 2, 3, 20, "f2")
    analyze_data()