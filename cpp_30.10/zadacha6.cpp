#include <iostream>
using namespace std;

int main() {
    int X;
    cin >> X;
    
    
    int tens = X / 10;
    

    int units = X % 10;
    
    cout << tens << " " << units << endl;
    
    return 0;
}