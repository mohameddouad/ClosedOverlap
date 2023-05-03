package douad.mining.patterns.constraints.overlap.topk;

import java.util.ArrayList;
import java.util.BitSet;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Entropy {

	private static int totalBitCodes;
	
	//constructor
	public Entropy(int totalBitCodes) {
        this.totalBitCodes = totalBitCodes;
    }
	
	public static int getNbBitCodes() {
		return totalBitCodes;
	}

	public  void setNbBitCodes(int totalBitCodes) {
		this.totalBitCodes = totalBitCodes;
	}
	
	
	public double calculateEntropy(List<BitSet> coversHistory) {
		
		// Transpose the coversHistory list
        List<BitSet> transposedCovers = transposeCovers(coversHistory);
        
        // Count the number of occurrences of each bit code
        HashMap<BitSet, Integer> bitCodeCounts = new HashMap<BitSet, Integer>();
        for (BitSet bitCode : transposedCovers) {
            int count = bitCodeCounts.getOrDefault(bitCode, 0);
            bitCodeCounts.put(bitCode, count + 1);            
        }
        
        System.out.println("Occurence number of each code: ");
        System.out.println(bitCodeCounts.toString());

        // Compute the probability of each bit code
        int totalBitCodes = transposedCovers.size();
        Map<BitSet, Double> bitCodeProbabilities = new HashMap<BitSet, Double>();
        for (Map.Entry<BitSet, Integer> entry : bitCodeCounts.entrySet()) {
            BitSet bitCode = entry.getKey();
            int count = entry.getValue();
            double probability = (double) count / totalBitCodes;
            bitCodeProbabilities.put(bitCode, probability);
        }

        // Calculate the entropy
        double entropy = 0.0;
        for (double probability : bitCodeProbabilities.values()) {
            entropy -= probability * log2(probability);
        }

        return entropy;
    }
	
	//Binary logarithm
	private double log2(double x) {
	    return Math.log(x) / Math.log(2);
	}
	
	//construct the transpose of the history from list of bit patterns (covers) to list of bit code
	private static List<BitSet> transposeCovers(List<BitSet> coversHistory) {
		//int totalBitCodes = getNbBitCodes();
        List<BitSet> transposedCovers = new ArrayList<>();
        for (int i = 0; i < totalBitCodes; i++) {
            BitSet column = new BitSet(coversHistory.size());
            for (int j = 0; j < coversHistory.size(); j++) {
                if (coversHistory.get(j).get(i)) {
                    column.set(j);
                }
            }
            transposedCovers.add(column);
        }
        return transposedCovers;
    }
	
	// Find the argMax entropy of history then inset the new candidate
	public void kMaximalEntropyInsert(List<BitSet> coversHistory, List<int[]> itemsetsHistory, BitSet coverCandidate, int[] itemsetCandidate, int k) {
	    
		if (coversHistory.size() < k) {
			
			itemsetsHistory.add(itemsetCandidate);
			coversHistory.add(coverCandidate);
			
		}else {
			
			double maxEntropy = calculateEntropy(coversHistory);
			System.out.println("max Entropy: "+ maxEntropy);
		    int maxEntropyIndex = -1;

		    // replacing each element in coversHistory with the candidate and calculate entropy
		    for (int i = 0; i < coversHistory.size(); i++) {
		        BitSet tempElement = coversHistory.get(i);
		        coversHistory.set(i, coverCandidate);
		        double entropy = calculateEntropy(coversHistory);
		        //System.out.println("max Entropy: "+ entropy);
		        if (entropy > maxEntropy) {
		            maxEntropy = entropy;
		            System.out.println("max Entropy: "+ maxEntropy);
		            maxEntropyIndex = i;
		        }
		        coversHistory.set(i, tempElement);
		    }

		    // If a replacement resulted in a max entropy, remove the corresponding element
		    if (maxEntropyIndex != -1) {
		    	
		    	itemsetsHistory.remove(maxEntropyIndex);
		    	itemsetsHistory.add(itemsetCandidate);
		    	
		        coversHistory.remove(maxEntropyIndex);
		        coversHistory.add(coverCandidate);
		    }
			
		}
	}
	
	// Find the argMax entropy of history then inset the new candidate in parallel
	public void kMaximalEntropyParallelInsert(List<BitSet> coversHistory, List<int[]> itemsetsHistory, BitSet coverCandidate, int[] itemsetCandidate, int k) {
	    
		if (coversHistory.size() < k) {
			
			itemsetsHistory.add(itemsetCandidate);
			coversHistory.add(coverCandidate);
			
		}else {
			
			double maxEntropy = calculateEntropy(coversHistory);
			System.out.println("max Entropy: "+ maxEntropy);
		    int maxEntropyIndex = -1;

		    // Try replacing each element in coversHistory with the candidate and calculate entropy in parallel
		    List<Double> entropies = coversHistory.parallelStream()
		            .map(element -> {
		                List<BitSet> newCoversHistory = new ArrayList<>(coversHistory);
		                int index = newCoversHistory.indexOf(element);
		                newCoversHistory.set(index, coverCandidate);
		                return calculateEntropy(newCoversHistory);
		            })
		            .collect(Collectors.toList());

		    // Find the maximum entropy and corresponding index
		    for (int i = 0; i < entropies.size(); i++) {
		        if (entropies.get(i) > maxEntropy) {
		            maxEntropy = entropies.get(i);
		            System.out.println("max Entropy: "+ maxEntropy);
		            maxEntropyIndex = i;
		        }
		    }

		    // If a replacement resulted in a lower entropy, remove the corresponding element
		    if (maxEntropyIndex != -1) {
		    	
		    	itemsetsHistory.remove(maxEntropyIndex);
		    	itemsetsHistory.add(itemsetCandidate);
		    	
		        coversHistory.remove(maxEntropyIndex);
		        coversHistory.add(coverCandidate);
		    }
		}
		
	}
	
	
	private static BitSet bitSetFromInts(int... ints) {
        BitSet bitSet = new BitSet(ints.length);
        for (int i = 0; i < ints.length; i++) {
            if (ints[i] != 0) {
                bitSet.set(i);
            }
        }
        return bitSet;
    }
	
	
	//Main function for testing
//	public static void main(String[] args) {
//	        // Initialize the data
//	        List<BitSet> coversHistory = new ArrayList<>();
////	        coversHistory.add(bitSetFromInts(1, 1, 1));
////	        coversHistory.add(bitSetFromInts(1, 1, 0));
////	        coversHistory.add(bitSetFromInts(1, 1, 1));
////	        coversHistory.add(bitSetFromInts(1, 0, 0));
////	        coversHistory.add(bitSetFromInts(0, 1, 1));
////	        coversHistory.add(bitSetFromInts(0, 0, 0));
////	        coversHistory.add(bitSetFromInts(0, 0, 1));
////	        coversHistory.add(bitSetFromInts(0, 0, 0));
//	        
//	        coversHistory.add(bitSetFromInts(1, 1, 1, 1, 0, 0, 0, 0));
//	        coversHistory.add(bitSetFromInts(1, 1, 1, 0, 1, 0, 0, 0));
//	        coversHistory.add(bitSetFromInts(1, 0, 1, 0, 1, 0, 1, 0));
//	        
//	        System.out.println("History size: " + coversHistory.size());
//	        
//	        Entropy entropyCalculator = new Entropy(8);
//	        double entropy = entropyCalculator.calculateEntropy(coversHistory);
//	        List<BitSet> transposedCovers = transposeCovers(coversHistory);
//	        
//	        System.out.println("transposedCovers size: " +transposedCovers.size());
//	        
//	        System.out.println("transposed Covers (bit codes): ");
//	        
//	     // Output the transposed covers
//	        for (BitSet column : transposedCovers) {
//	            StringBuilder sb = new StringBuilder();
//	            for (int i = 0; i < coversHistory.size(); i++) {
//	                if (column.get(i)) {
//	                    sb.append("1");
//	                } else {
//	                    sb.append("0");
//	                }
//	            }
//	            System.out.println(sb.toString());
//	        }
//	        
//	        //System.out.println("transposedCovers: " + transposedCovers.size());
//	        System.out.println("Entropy: " + entropy);
//	    }
	
}
