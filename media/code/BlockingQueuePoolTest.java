// Copyright (c) 2005  Dustin Sallings <dustin@spy.net>

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.ArrayList;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CountDownLatch;

public class BlockingQueuePoolTest extends Thread {

	public enum Mode {
		POOL, NEW, LOCKED
	}

	private static final String TSTRING="2006-11-09T01:16:13";
	private static final String FORMAT="yyyy-MM-dd'T'HH:mm:ss";

	private BlockingQueue<SimpleDateFormat> fmts=null;
	private SimpleDateFormat sdf=null;
	private CountDownLatch latch=null;
	private Mode mode=null;

	/**
	 * Get an instance of BlockingQueuePoolTest.
	 */
	public BlockingQueuePoolTest(Mode m, SimpleDateFormat f,
		BlockingQueue<SimpleDateFormat> fs, CountDownLatch l) {
		super("BlockingQueuePoolTest");
		mode=m;
		sdf=f;
		fmts=fs;
		latch=l;
		setDaemon(true);
		start();
	}

	public void run() {
		try {
			latch.countDown();
			latch.await();
			for(int i=0; i<1000; i++) {
				switch(mode) {
					case POOL:
						runWithPool();
						break;
					case NEW:
						runWithNew();
						break;
					case LOCKED:
						runWithLock();
				}
			}
		} catch(Exception e) {
			e.printStackTrace();
		}
	}

	private void transform(SimpleDateFormat sdf) throws Exception {
		Date d=sdf.parse(TSTRING);
		String s=sdf.format(d);
		assert s.equals(TSTRING) : "Strings don't match.";
	}

	private void runWithLock() throws Exception {
		synchronized(sdf) {
			transform(sdf);
		}
	}

	private void runWithNew() throws Exception {
		transform(new SimpleDateFormat(FORMAT));
	}

	private void runWithPool() throws Exception {
		SimpleDateFormat sdf=fmts.take();
		assert sdf != null;
		try {
			transform(sdf);
		} finally {
			fmts.add(sdf);
		}
	}

	private static void doTest(int nThreads, Mode mode) throws Exception {
		SimpleDateFormat sdf=new SimpleDateFormat(FORMAT);
		BlockingQueue<SimpleDateFormat> fs=
			new ArrayBlockingQueue<SimpleDateFormat>(10);
		for(int i=0; i<10; i++) {
			fs.add((SimpleDateFormat)sdf.clone());
		}

		System.out.println(nThreads + " threads, " + fs.size()
			+ " in pool, mode: " + mode);

		CountDownLatch cdl=new CountDownLatch(nThreads+1);

		ArrayList<BlockingQueuePoolTest> qs=
			new ArrayList<BlockingQueuePoolTest>();
		for(int i=0; i<nThreads; i++) {
			qs.add(new BlockingQueuePoolTest(mode, sdf, fs, cdl));
		}

		long start=System.currentTimeMillis();
		cdl.countDown();
		for(BlockingQueuePoolTest q : qs) {
			q.join();
		}
		long end=System.currentTimeMillis();

		System.out.println("Processing time:  " + (end-start) + "ms");
	}

	public static void main(String[] args) throws Exception {
		for(Mode m : Mode.values()) {
			doTest(5, m);
			doTest(15, m);
		}
		System.out.println("\n*** Warmed up, running the real test now ***\n");
		for(Mode m : Mode.values()) {
			doTest(5, m);
			doTest(15, m);
		}
	}

}
