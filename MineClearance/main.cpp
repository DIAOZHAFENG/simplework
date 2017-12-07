#include <iostream>
#include "MineClearance.h"

using namespace std;

int main() {
    cout << "input map size(width and height) and mine count: " << endl;
    int width, height, mine;
    cin >> width >> height >> mine;
    try{
        MineClearance mc(width, height, mine);
        int x, y, mode;
        int explore_res = 0;
        while (explore_res == 0) {
            mc.drawMap();
            cout << "input coordinate(x and y) and operation mode(0 for explore the area, 1 for mark it): " << endl;
            cin >> x >> y >> mode;
            if (mode == 0) {
                explore_res = mc.explore(x, y);
                if (explore_res == -1) {
                    mc.drawMap();
                    cout << "BOOM SHAKALAKA!!!" << endl;
                }
                else if (explore_res == 1) {
                    mc.drawMap();
                    cout << "CLEAR!" << endl;
                }
            }
            else if (mode == 1) {
                mc.mark(x, y);
            }
        }
    }
    catch (int n){
        cout << "play by rule! " << n << endl;
    }
    return 0;
}
