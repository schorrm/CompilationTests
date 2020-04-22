#ifndef _236360_2_
#define _236360_2_

#include <string>
using namespace std;

namespace output {
	extern const string rules[];
    void printProductionRule(int ruleno);
    void errorLex(int lineno);
    void errorSyn(int lineno);
};

#endif
