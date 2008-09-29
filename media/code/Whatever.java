import java.util.ArrayList;
import java.util.Collection;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.atomic.AtomicReference;

public class Whatever {

	private static Whatever instance=null;
	private static AtomicReference<Whatever> instanceRef=
		new AtomicReference<Whatever>(null);

	public static synchronized Whatever getInstance() {
		if(instance == null) {
			instance=new Whatever();
		}
		return instance;
	}

	public static synchronized void setInstance(Whatever to) {
		instance=to;
	}

	public static synchronized Whatever getInstance2() {
		Whatever rv=instanceRef.get();
		if(rv == null) {
			synchronized(Whatever.class) {
				rv=instanceRef.get();
				if(rv == null) {
					rv=new Whatever();
					boolean changed=instanceRef.compareAndSet( null, rv);
					// Just a reminder, assert means stating
					// something that isn't supposed to be possible.
					assert changed : "Race condition updating singleton";
				}
			}
		}
		return rv;
	}

	public static synchronized void setInstance2(Whatever to) {
		instanceRef.set(to);
	}

	public static void main(String args[]) throws Exception {
		int total=Integer.parseInt(args[0]);
		Map<String, Collection<Long>> results=
			new TreeMap<String, Collection<Long>>();
		int nThreads=4;

		System.out.println(total + " total requests, "
			+ nThreads + " threads for MT test");

		for(int i=0; i<5; i++) {
			System.out.print("+");
			runTest(results, "Synchronized", total, nThreads, new Runnable() {
					public void run() { Whatever.getInstance(); }
					});
			runTest(results, "Atomics", total, nThreads, new Runnable() {
					public void run() { Whatever.getInstance2(); }
					});
		}

		System.out.println("\nResults:");
		for(Map.Entry<String, Collection<Long>> me : results.entrySet()) {
			System.out.println(" " + me.getKey() + "\n\t" + me.getValue());
		}
	}

	private static void runTest(Map<String, Collection<Long>> results,
		String name, int total, int nThreads, Runnable r) throws Exception {

		System.out.print(".");
		Whatever.setInstance(null);
		Whatever.setInstance2(null);
		long start=System.currentTimeMillis();
		mainSingle(total, r);
		report(results, name + ".st", start);

		System.out.print(".");
		Whatever.setInstance(null);
		Whatever.setInstance2(null);
		start=System.currentTimeMillis();
		mainThreaded(total, nThreads, r);
		report(results, name + ".mt", start);
	}

	private static void report(Map<String, Collection<Long>> results,
		String key, long start) {
		long end=System.currentTimeMillis();
		Collection<Long> c=results.get(key);
		if(c == null) {
			c=new ArrayList<Long>();
			results.put(key, c);
		}
		c.add(end-start);
	}

	public static void mainSingle(int total, Runnable r) {
		for(int i=0; i<total; i++) {
			r.run();
		}
	}

	public static void mainThreaded(int total, int numThreads,
			Runnable r) throws Exception {
		Collection<Thread> c=new ArrayList<Thread>();
		for(int i=0; i<numThreads; i++) {
			c.add(new GetThread(total/numThreads, r));
		}
		for(Thread t : c) {
			t.start();
		}
		for(Thread t : c) {
			t.join();
		}
	}

	private static class GetThread extends Thread {
		private int todo=0;
		private Runnable r=null;
		public GetThread(int n, Runnable runnable) {
			todo=n;
			r=runnable;
		}
		public void run() {
			for(int i=0; i<todo; i++) {
				r.run();
			}
		}
	}

}
