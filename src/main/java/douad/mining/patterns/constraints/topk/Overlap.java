package douad.mining.patterns.constraints.topk;

import io.gitlab.chaver.mining.patterns.io.Database;

import org.chocosolver.solver.Cause;
import org.chocosolver.solver.constraints.Propagator;
import org.chocosolver.solver.exception.ContradictionException;
import org.chocosolver.solver.search.loop.monitors.IMonitorSolution;
import org.chocosolver.solver.variables.BoolVar;
import org.chocosolver.solver.variables.IntVar;
import org.chocosolver.util.ESat;

import java.util.*;
import java.util.stream.IntStream;

public class Overlap extends Propagator<IntVar> implements IMonitorSolution {

    private Database database;
    private BitSet[] verticalRepresentation;
    private Entropy entropy;
    private BoolVar[] x;
    static double Tmax;
    private int theta;
    private final int k;
    private boolean parallel;
    private List<int[]> itemsetsHistory = new ArrayList<>();
    private List<BitSet> coversHistory = new ArrayList<>();

    public Overlap(Database database, BoolVar[] x, double Tmax, int theta, int k, boolean parallel) {
        super(x);
        this.database = database;
        this.verticalRepresentation = database.getVerticalRepresentation();
        this.x = x;
        this.Tmax = Tmax; //threshold of diversity
        this.theta = theta;
        this.k = k;
        this.parallel = parallel;
    }

    private BitSet createCover() {
        BitSet cover = new BitSet(database.getNbTransactions());
        cover.set(0, database.getNbTransactions());
        return cover;
    }

    private BitSet computeCoverUnion(BitSet cover, BitSet cover2) {
        BitSet coverUnion = (BitSet) cover.clone();
        coverUnion.and(cover2);
        return coverUnion;
    }

    //test if pattern1 included in pattern2
    public boolean inclusion(BitSet pattern1, BitSet pattern2) {
		BitSet p = new BitSet();
		p = (BitSet) pattern1.clone();
		p.andNot(pattern2);

		if (p.isEmpty()) {
			return true;
		}
		return false;
	}
    
    //lower bound
    private double LBOverlap(BitSet xCover, BitSet HCover) {
        BitSet inter = (BitSet) xCover.clone();
        inter.and(HCover);
        int properCoverCardinality = xCover.cardinality() - inter.cardinality();
        //double LB = (double) (theta - properCoverCardinality) / (xCover.cardinality() + HCover.cardinality());
        double LB = (double) (theta - properCoverCardinality) / Math.min(xCover.cardinality(), HCover.cardinality());
        return (double) Math.max(LB, 0);
    }
    
    //upper bound
    private double UBOverlap(BitSet xCover, BitSet HCover) {
        BitSet inter = (BitSet) xCover.clone();
        inter.and(HCover);
        //int properCoverCardinality = xCover.cardinality() - inter.cardinality();
        //double LB = (double) (theta - properCoverCardinality) / (xCover.cardinality() + HCover.cardinality());
        double UB = (double) inter.cardinality() / theta;
        return (double) Math.min(UB, 1);
    }
    
    private boolean PGrowthLB(BitSet xCover) {
        for (BitSet HCover : coversHistory) {
            if (LBOverlap(xCover, HCover) > Tmax) {
                return false;
            }
        }
        return true;
    }


    @Override
    public void propagate(int evtmask) throws ContradictionException {
        BitSet xCover = createCover();
        
        Set<Integer> freeItems = new HashSet<>();
        Set<Integer> positifItems = new HashSet<>();
        Set<Integer> negatifItems = new HashSet<>();
        
        for (int i = 0; i < database.getNbItems(); i++) {
            if (x[i].isInstantiatedTo(1)) {
                xCover.and(verticalRepresentation[i]);
                positifItems.add(i);
            }else if (x[i].isInstantiatedTo(0)) {
            	negatifItems.add(i);
            }
            else /*(!x[i].isInstantiated())*/ {
                freeItems.add(i);
            }
        }
        
        // calcul de la couverture courante de positif items
        
        // Fails if x+ is not diversified
        if (!positifItems.isEmpty() && !PGrowthLB(xCover)) {
        	//model.getSolver().setJumpTo(1);
            fails();
        }
        
        for (int i : freeItems) {
        	
        	//lower bound of overlap
            if (!PGrowthLB(computeCoverUnion(xCover, verticalRepresentation[i]))) {
            	x[i].removeValue(1, Cause.Null);
                //x[i].setToFalse(this);
            	negatifItems.add(i);
            	continue;
            }
            
            //filter by implications  
            BitSet xCover_u_i = computeCoverUnion(xCover, verticalRepresentation[i]);
            for (int k : negatifItems) {
            	// test if cover of "positifItems U {k}" contains cover of "positifItems U {i}"
            	BitSet xCover_u_k = computeCoverUnion(xCover, verticalRepresentation[k]);
            	if (inclusion(xCover_u_i, xCover_u_k)) {
					x[i].removeValue(1, Cause.Null);
					negatifItems.add(i);
					break;
				}
            }
        }
    }

    @Override
    public ESat isEntailed() {
        return ESat.UNDEFINED;
    }

    @Override
    public void onSolution() {
        int[] itemsetCandidate = IntStream
                .range(0, database.getNbItems())
                .filter(i -> x[i].getValue() == 1)
                .toArray();
        
        BitSet coverCandidate = createCover();
        for (int i : itemsetCandidate) {
            coverCandidate.and(verticalRepresentation[i]);
        }
        
        int totalBitCodes = database.getNbTransactions();
        entropy = new Entropy(totalBitCodes);
        
        if (!parallel) {
        	
        	entropy.kMaximalEntropyInsert(coversHistory, itemsetsHistory, coverCandidate, itemsetCandidate, k);
		
        }else {
			
			entropy.kMaximalEntropyParallelInsert(coversHistory, itemsetsHistory, coverCandidate, itemsetCandidate, k);
		
        }        
        
    }

    
    public List<int[]> getItemsetsHistory() {
        return itemsetsHistory;
    }

    public List<BitSet> getCoversHistory() {
        return coversHistory;
    }
    
    public static double computeOverlap(BitSet cov, BitSet cov2) {
        BitSet inter = (BitSet) cov.clone();
        inter.and(cov2);        
        return (double) inter.cardinality() / Math.min(cov.cardinality(), cov2.cardinality());
    }
    
}