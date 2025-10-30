#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

int main() {
    const double PI = 3.14159265359;
    double R;
    cin >> R;
    

    double volume = (4.0 / 3.0) * PI * pow(R, 3);
    
 
    cout << fixed << setprecision(3);
    cout << volume << endl;
    
    return 0;
}