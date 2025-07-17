#include <iostream>
#include <cstdlib>
#include <vector>
#include <chrono>
#include <cmath>
#include <random>

using namespace std;

class Diagram {
    vector<int> columns;
    vector<double> poss_moves_weight;
    vector<int> poss_moves_column;


    public:
    Diagram() {
        columns = {1};
        poss_moves_weight.reserve(5000);   // suponiendo que no tendremos más de 5000 columnas
        poss_moves_column.reserve(5000);
    }

    ~Diagram() {}

    inline double get_S(int x, int y, double alpha) {
        double perimeter = (x + y + 2) * 2.0;
        return pow(perimeter, alpha);
    }

    int select_move(vector<double>& weights, vector<int>& options, std::mt19937& gen) {
        std::discrete_distribution<> dist(weights.begin(), weights.end());
        return options[dist(gen)];
    }

    int get_new_cell(int alpha, std::mt19937& gen) {
        poss_moves_weight.clear();
        poss_moves_column.clear();
        double total_s = 0.0;
        int s_value;
        for (int x = 0; x < columns.size(); x++)
        {
            if (x == 0)
            {
                s_value = get_S(x, columns[x], alpha);
                poss_moves_weight.push_back(s_value);
                poss_moves_column.push_back(x);
                continue;
            }

            if (columns[x-1] > columns[x])
            {
                s_value = get_S(x, columns[x-1], alpha);
                poss_moves_weight.push_back(s_value);
                poss_moves_column.push_back(x);
            }


        }
        s_value = get_S(columns.size(), 0, alpha);
        poss_moves_weight.push_back(s_value);
        poss_moves_column.push_back(columns.size());

        return select_move(poss_moves_weight, poss_moves_column, gen);
    }

    int simulate_young_diagram(int n, int alpha, std::mt19937& gen) {
        for (int i = 0; i < n; i++)
        {
            int selected_column = get_new_cell(alpha, gen);
            if (selected_column == columns.size())
            {
                columns.push_back(1);
            } else
            {
                columns[selected_column] += 1;
            }
        }
        return columns.size();
    }
};

int main() 
{
    int m, n, alpha;
    cout << "Enter the number of repetitions (m): ";
    cin >> m;
    cout << "Enter the number of cells (n): ";
    cin >> n;
    cout << "Enter the value of alpha: ";
    cin >> alpha;

    std::random_device rd;
    std::mt19937 gen(rd());

    auto start = chrono::high_resolution_clock::now();
    double result = 0;
    const double n_sqrt = sqrt(n); 

    for (int i = 0; i < m; i++)
    {
        Diagram diagram;
        int l_value = diagram.simulate_young_diagram(n, alpha, gen);
        result += (l_value - result) / (i + 1);
    }
    result /= n_sqrt;

    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::seconds>(end - start);

    cout << "Average size of the diagram: " << result << endl;
    cout << "Time taken: " << duration.count() << " seconds" << endl;
 
    return 0;
}