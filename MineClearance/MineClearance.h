//
// Created by shudingwen on 2016/9/26.
//

#ifndef HELLOWORLD_MINECLEARANCE_H
#define HELLOWORLD_MINECLEARANCE_H

#endif //HELLOWORLD_MINECLEARANCE_H

using namespace std;

class Lattice {
private:
    int stat; // -1 for unknown; 0 for marked; 1 for explored
    int count; // -1 for there is a mine; else for the mine count around
public:
    Lattice(): stat(-1), count(0) {}

    Lattice(int count): stat(-1), count(count) {}

    int getStat() {
        return this->stat;
    }

    int explore() {
        if (this->stat == -1) {
            this->stat = 1;
            return getCount();
        }
    }

    void mark() {
        if (this->stat == -1) {
            this->stat = 0;
        }
        else if (this->stat == 0) {
            this->stat = -1;
        }
    }

    int getCount() {
        return this->count;
    }

    void addCount() {
        if (this->count >= 0){
            (this->count)++;
        }
    }

    void setMine() {
        this->count = -1;
    }
};

class MineClearance {
private:
    int a = 0; // width
    int b = 0; // height
    int mine = 0; // mine count
    int explored = 0; // explored lattice count
    vector<Lattice> map;

    vector<int> getRandomNumbers(int n, int range);

    Lattice &getLattice(int x, int y) {
        if (x >= a || x < 0) {
            cout << "over wide" << endl;
            throw x;
        }
        else if (y >= b || y < 0) {
            cout << "over high" << endl;
            throw y;
        }
        return map[x + a * y];
    }

    Lattice &getLattice(int idx) {
        if (idx >= a * b) {
            cout << "index out of bound" << endl;
            throw idx;
        }
        return map[idx];
    }

    vector<int> getLatticeAround(int idx);

    int explore(int idx);

    int getStat(int idx) {
        return getLattice(idx).getStat();
    }

    void initMap();

public:
    MineClearance(int a, int b, int mine): a(a), b(b), mine(mine) {
        if (mine >= a * b) {
            cout << "instantiate error" << endl;
            throw mine;
        }
        initMap();
    }

    int explore(int x, int y);

    void mark(int x, int y) {
        getLattice(x, y).mark();
    }

    void drawMap();
};
