#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    double a, b, c;
    cin >> a >> b >> c;
    
    // Находим минимальную цену среди трех швабр
    double min_price = min({a, b, c});
    
    // Вычисляем сдачу
    double change = 1000.0 - min_price;
    
    cout << change << endl;
    
    return 0;
}