import java.util.ArrayList;
import java.util.Collection;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.atomic.AtomicReference;

public class Whatever2 {

	private static Whatever2 instance=null;
	private static AtomicReference<Whatever2> instanceRef=
		new AtomicReference<Whatever2>(null);
	private volatile static Whatever2 instanceVol=null;

	public static synchronized Whatever2 getInstance() {
		if(instance == null) {
			instance=new Whatever2();
		}
		return instance;
	}

	public static synchronized void setInstance(Whatever2 to) {
		instance=to;
	}

	public static synchronized Whatever2 getInstance2() {
		Whatever2 rv=instanceRef.get();
		if(rv == null) {
			synchronized(Whatever2.class) {
				rv=instanceRef.get();
				if(rv == null) {
					rv=new Whatever2();
					boolean changed=instanceRef.compareAndSet( null, rv);
					// Just a reminder, assert means stating
					// something that isn't supposed to be possible.
					assert changed : "Race condition updating singleton";
				}
			}
		}
		return rv;
	}

	public static synchronized void setInstance2(Whatever2 to) {
		instanceRef.set(to);
	}

	public static Whatever2 getInstanceVol() {
		if(instanceVol == null) {
			synchronized(Whatever2.class) {
				if(instanceVol == null) {
					instanceVol=new Whatever2();
				}
			}
		}
		return instanceVol;
	}

	public static synchronized void setInstanceVol(Whatever2 to) {
		instanceVol=to;
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
					public void run() { Whatever2.getInstance(); }
					});
			runTest(results, "Atomics", total, nThreads, new Runnable() {
					public void run() { Whatever2.getInstance2(); }
					});
			runTest(results, "Volatile", total, nThreads, new Runnable() {
					public void run() { Whatever2.getInstanceVol(); }
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
		Whatever2.setInstance(null);
		Whatever2.setInstance2(null);
		long start=System.currentTimeMillis();
		mainSingle(total, r);
		report(results, name + ".st", start);

		System.out.print(".");
		Whatever2.setInstance(null);
		Whatever2.setInstance2(null);
		Whatever2.setInstanceVol(null);
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
