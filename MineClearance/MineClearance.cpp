//
// Created by shudingwen on 2016/9/26.
//

#include <iostream>
#include <vector>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "MineClearance.h"

using namespace std;


vector<int> MineClearance::getRandomNumbers(int n, int range) {
    if (n >= range) {
        cout << "generate random mine error" << endl;
        throw n;
    }
    vector<int> res;
    int numbers[range];
    // init numbers collection
    for (int i=0; i<range; i++) {
        numbers[i] = i;
    }
    srand((unsigned int)(time(NULL)));
    for (int i=0; i<n; i++) {
        int randomIdx = rand() % range;
        res.push_back(numbers[randomIdx]);
        numbers[randomIdx] = numbers[range--];
    }
    return res;
}

vector<int> MineClearance::getLatticeAround(int idx) {
    vector<int> area;
    int up = -1;
    int down = 1;
    int left = -1;
    int right = 1;
    if (idx - a < 0) {
        up = 0;
    }
    if (idx + a >= a * b) {
        down = 0;
    }
    if (idx % a == 0) {
        left = 0;
    }
    if ((idx + 1) % a == 0) {
        right = 0;
    }
    int index;
    for (int i=up; i <= down; i++) {
        for (int j=left; j <= right; j++) {
            index = idx + i * a + j;
            if (index != idx && getStat(index) == -1) {
                area.push_back(index);
            }
        }
    }
    return area;
}

int MineClearance::explore(int idx) {
    if (getStat(idx) == -1) {
        explored++;
    }
    int mine = getLattice(idx).explore();
    if (mine == 0) {
        for (int l : getLatticeAround(idx)) {
            explore(l);
        }
    }
    return mine;
}

void MineClearance::initMap() {
    vector<int> mines = getRandomNumbers(mine, a * b);
    for (int i=0; i<a*b; i++) {
        map.push_back(Lattice());
    }
    for (int m : mines) {
        getLattice(m).setMine();
        for (int l : getLatticeAround(m)) {
            getLattice(l).addCount();
        }
    }
}

int MineClearance::explore(int x, int y) {
    int idx = x + a * y;
    if (getStat(idx) == -1) {
        if (explore(idx) < 0) {
            // game over
            return -1;
        }
        else if (explored + mine == a * b) {
            // win
            return 1;
        }
        cout << "explored: " << explored << "mine: " << mine << "a*b: " << a*b << endl;
    }
    return 0;
}

void MineClearance::drawMap() {
    for (vector<Lattice>::size_type i=0; i<map.size(); i++) {
        Lattice l = getLattice(i);
        int stat = l.getStat();
        if (stat == -1) {
            cout << "* ";
        }
        else if (stat == 0) {
            cout << "M ";
        }
        else if (stat == 1) {
            if (l.getCount() < 0) {
                cout << "X ";
            }
            else {
                cout << l.getCount() << " ";
            }
        }
        if ((i + 1) % a == 0) {
            cout << "\n";
        }
    }
    cout << endl;
}
