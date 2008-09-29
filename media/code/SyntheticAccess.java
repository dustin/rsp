// Copyright (c) 2006  Dustin Sallings <dustin@spy.net>

import java.util.Iterator;
import java.util.Collection;
import java.util.ArrayList;
import java.util.Map;
import java.util.TreeMap;

/**
 * Test synthetic access performance.
 */
public class SyntheticAccess extends Object {

	/**
	 * Get an instance of SyntheticAccess.
	 */
	public SyntheticAccess() {
		super();
	}

	private static void report(Map m, String name, long start) {
		long end=System.currentTimeMillis();
		Collection c=(Collection)m.get(name);
		if(c == null) {
			c=new ArrayList();
			m.put(name, c);
		}
		c.add(new Long(end-start));
	}

	public static void main(String args[]) throws Exception {
		int n=Integer.parseInt(args[0]);
		System.out.println("Running " + n + " iterations 5 times each.");

		Inner inner=new Inner();
		Map m=new TreeMap();
		for(int o=0; o<5; o++) {
			inner.synthField=0;
			inner.visibleField=0;

			long start=System.currentTimeMillis();
			for(int i=0; i<n; i++) {
				inner.syntheticMethod();
			}
			report(m, "synth method", start);

			start=System.currentTimeMillis();
			for(int i=0; i<n; i++) {
				inner.visibleMethod();
			}
			report(m, "pkg visible method", start);

			start=System.currentTimeMillis();
			for(int i=0; i<n; i++) {
				int x=inner.synthField++;
			}
			report(m, "synth field", start);

			start=System.currentTimeMillis();
			for(int i=0; i<n; i++) {
				int x=inner.visibleField++;
			}
			report(m, "pkg visible field", start);
		}
		for(Iterator i=m.entrySet().iterator(); i.hasNext(); ) {
			Map.Entry me=(Map.Entry)i.next();
			System.out.println(me.getKey() + ": " + me.getValue());
		}
	}

	private static class Inner {
		private int synthField=0;
		int visibleField=0;

		// Note that under 1.5 -server, my synthetic method call was optimized
		// *completely* out.  After the first run through the loop, I was
		// registering 0ms for 1,000,000,000 iterations.  This was not the case
		// for the visible method.

		private void syntheticMethod() {
			// trivial work to avoid getting optimized out
			synthField--;
		}
		void visibleMethod() {
			// trivial work to avoid getting optimized out
			visibleField--;
		}
	}

}
