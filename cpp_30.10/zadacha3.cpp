#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

int main() {
    double n;
    cin >> n;
    
    
    double rounded = round(n * 100) / 100;
    
  
    cout << fixed << setprecision(2);
    cout << rounded << endl;
    
    return 0;
}