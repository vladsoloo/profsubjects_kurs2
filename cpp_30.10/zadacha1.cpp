#include <iostream>
#include <iomanip>

int main() {
    double a, b;
    std::cin >> a >> b;
    
    double result = 1.0 / (1.0 + (a + b) / 2.0);
    
    std::cout << std::fixed << std::setprecision(5);
    std::cout << result << std::endl;
    
    return 0;
}
