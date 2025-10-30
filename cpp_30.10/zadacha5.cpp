#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
using namespace std;

int main() {
    double X;
    cin >> X;
    
   
    stringstream ss;
    ss << fixed << setprecision(2) << X;
    string str = ss.str();
    
  
    size_t dot_pos = str.find('.');
    
   
    string after_dot = str.substr(dot_pos + 1);
    int result = stoi(after_dot);
    
    cout << result << endl;
    
    return 0;
}