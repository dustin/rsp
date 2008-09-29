public class PerfTest extends Object {

	private static int someNumber=0;

	private static void mutateFunction() {
		someNumber++;
	}

	private static void loopFunction(int n) {
		int i=0;
		for(i=0; i<n; i++) {
			mutateFunction();
		}
	}

	public static void main(String[] args) {
		int innerLoops=0, outerLoops=0, i=0;

		outerLoops=Integer.parseInt(args[0]);
		innerLoops=Integer.parseInt(args[1]);

		for(i=0; i<outerLoops; i++) {
			someNumber=0;
			loopFunction(innerLoops);
			assert someNumber == innerLoops;
		}
	}

}

