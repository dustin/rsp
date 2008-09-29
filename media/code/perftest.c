#include <assert.h>
#include <stdlib.h>

static int someNumber=0;

void mutateFunction() {
	someNumber++;
}

void loopFunction(int n) {
	int i=0;
	for(i=0; i<n; i++) {
		mutateFunction();
	}
}

int main(int argc, char **argv) {
	int innerLoops=0, outerLoops=0, i=0;
	assert(argc > 2);

	outerLoops=atoi(argv[1]);
	innerLoops=atoi(argv[2]);

	for(i=0; i<outerLoops; i++) {
		someNumber=0;
		loopFunction(innerLoops);
		assert(someNumber == innerLoops);
	}
	return 0;
}
