#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

int main() {
    double n;
    cin >> n;
    
    // Округляем до двух знаков после запятой
    double rounded = round(n * 100) / 100;
    
    // Выводим с фиксированной точностью и 2 знаками после запятой
    cout << fixed << setprecision(2);
    cout << rounded << endl;
    
    return 0;
}