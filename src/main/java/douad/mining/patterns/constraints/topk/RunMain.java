package douad.mining.patterns.constraints.topk;

import io.gitlab.chaver.mining.patterns.constraints.*;
import io.gitlab.chaver.mining.patterns.io.DatReader;
import io.gitlab.chaver.mining.patterns.io.Database;
import io.gitlab.chaver.mining.patterns.io.Pattern;
import io.gitlab.chaver.mining.patterns.search.strategy.selectors.variables.MinCov;
import org.chocosolver.solver.Model;
import org.chocosolver.solver.Solver;
import org.chocosolver.solver.constraints.Constraint;
import org.chocosolver.solver.search.strategy.Search;
//import org.chocosolver.solver.search.strategy.selectors.values.IntDomainMin;
//import org.chocosolver.solver.search.strategy.selectors.variables.InputOrder;
import org.chocosolver.solver.variables.BoolVar;
import org.chocosolver.solver.variables.IntVar;

import douad.mining.patterns.search.strategy.selectors.variables.IntDomainMax;

//import contraintes.closedpattern.MemoryLogger;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.BitSet;
import java.util.List;
import java.util.stream.IntStream;

//import contraintes.closedpattern.diversity.DataSet;
//import contraintes.closedpattern.diversity.diversity_overlap.MinCov;

public class RunMain {
	
	static String[] argparam;
	public static String pathInput;
	public static String pathOutput;
	public static String pathAnalyse;
	
	public static int theta;
	
	static double Tmax;
	public static int k;
	public static boolean parallel = false;  
	
	static Database database;
	static List<int[]> itemsets;
	static List<BitSet> covers;
	
	public static BufferedWriter writer;
	
	
	private static String formatCover(BitSet cov) {
		String s = "";
		for (int tr = cov.nextSetBit(0); tr != -1; tr = cov.nextSetBit(tr + 1)) {
			s += "" + (tr + 1) + " ";
		}
		if (!s.isEmpty())
			s = s.substring(0, s.length() - 1);
		return s;
	}

	
	public static void getSolutionsWithCover(FileWriter fr) {
		for (int i = 0; i < itemsets.size(); i++) {
			String s = "";
			int[] itemset = Arrays.stream(itemsets.get(i))
                    .map(j -> database.getItems()[j])
                    .toArray();
			StringBuilder builder = new StringBuilder();
			for (int value : itemset) {
			    builder.append(value);
			}
			s += "[ " + i + " ] ";
			s += "[ ";
			//s += "" + Arrays.toString(itemset) + " ";
			s += "" + builder.toString() + " ";
			s += "] ";
			
			//covers
			//s += "[ " + covers.get(i) + " ] ";
			s += "[ " + formatCover(covers.get(i)) + " ] ";
			s += "[ " + covers.get(i).cardinality()	+ " ]\n";
			try {
				fr.write(s);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				System.out.println("Error occured when writing solutions.");
				e.printStackTrace();
			}
		}
	}
	
	
	public static void FilesResults(Solver s, List<int[]> itemsets, List<BitSet> covers) throws IOException {
		
		//Solver s = model.getSolver();

		double cpu_time = 0.0;
		long nb_nodes = 0;
		long nb_solutions = 0;

		//MemoryLogger.getInstance().reset();
			
		writer = new BufferedWriter(new FileWriter(pathOutput));
		StringBuilder buffer = new StringBuilder();
		String solution = "";
		
		cpu_time = s.getTimeCount();
		nb_nodes = s.getNodeCount();
		nb_solutions = s.getSolutionCount();

		/*
		 * **********************************************************************
		 * **********************************************************************
		 */

		buffer.append(solution);
		
		writer.write(buffer.toString());
		writer.close();
		
		
		File datasetFile = new File(pathInput);
		File outputFile = new File(pathOutput);
		
		String output_data = "" + datasetFile.getName() + ";" + outputFile.getName() + ";" +
				((double) theta/database.getNbTransactions()) + ";" + Tmax + ";" + cpu_time +
				";" + nb_solutions + ";" + nb_nodes + ";" + "\n";
		
		File file = new File(pathAnalyse);
		FileWriter fr;
		
		
		fr = new FileWriter(file, false);
		fr.write(output_data);
		fr.close();
		
		
		file = new File(pathOutput);
		//System.out.println(file);
		
		
		fr = new FileWriter(file, false);
		getSolutionsWithCover(fr);
		fr.close();
	
		
		System.out.println("\n************\n");
		
		MemoryLogger.getInstance().checkMemory();

		System.out.println("Jmax final = " + Overlap.Tmax);
		System.out.println("K Pattern = " + k);
		System.out.println("durée = " + s.getTimeCount());
		//System.out.println("max memory = " + MemoryLogger.getInstance().getMaxMemory());
		System.out.println("nb total de solutions = " + s.getSolutionCount());
		System.out.println("nb total de noeuds = " + s.getNodeCount());
		System.out.println("nb total d'échecs = " + s.getFailCount());
		//System.out.println("nb de solutions witness = " + this.nbTotalWitnessSolutions);
		//System.out.println("nb d'items filtrés par LB = " + this.cd.numberVarFiltredByLB);
		//System.out.println("\nnb de noeuds witness = " + nb);
		//System.out.println("nb appels UB = " + nbAppel);
		System.out.println("***** END *****");
	}
	
    public static void main(String[] args) throws Exception {
    	argparam = args;
//        //String dataPath = "data/charm.dat";
//    	String dataPath = "data/hepatitis.dat";
//        //String dataPath = "src/test/resources/contextPasquier99/contextPasquier99.dat";
        Model model = new Model("Diversity");
//        Database database = new DatReader(dataPath, 0, true).readFiles();
//        //int theta = (int) Math.round(database.getNbTransactions() * 0.01d);
//        //int theta = (int) Math.round((database.getNbTransactions() /100) * 30);
//        int theta = 42;//0.2
		
		//try {
			
			// getting the data
			pathInput = argparam[0]; // input file
			pathOutput = argparam[1]; // output file
			pathAnalyse = argparam[2]; // output analysis file
			
			// theta = Integer.parseInt(argparam[1]);
			if(argparam[3].equals("-f"))
				theta = Integer.valueOf(argparam[4]);
			else {
				theta = Integer.valueOf("error");
			}

//		} catch (NumberFormatException e) {
//			System.out.println("Error: the minimal frequency threshold should be an integer.");
//			e.printStackTrace();
//			System.exit(1);
//		}
	    
	    // Determine whether it's TopK or not and diversity
 		//try {
 			if(argparam[5].equals("-t")) {
 				Tmax = Double.valueOf(argparam[6]);
 			}
 			else {
 				Tmax = Double.valueOf("error");
 			}
 			
 			if(argparam[7].equals("-topk")) {
 				k = Integer.valueOf(argparam[8]);
 				
 				if(argparam[9].equals("-th")) {
 	 				parallel = true;
 	 			}
 	 			else {
 	 				k = Integer.valueOf("error");
 	 			}
 			}
 			else {
 				k = Integer.valueOf("error");
 			}

 		//} catch (NumberFormatException e) {
 			//System.out.println("Error: the maximum diversity threshold should be a double.");
 			//e.printStackTrace();
 			//System.exit(1);
 		//}
 		
 		// dataset initialization
		database = new DatReader(pathInput, 0, true).readFiles();
		System.out.println(pathInput);
    	
        System.out.println("theta = "+theta+" transaction number = "+database.getNbTransactions());
        
        IntVar freq = model.intVar("freq", theta, database.getNbTransactions());
        IntVar length = model.intVar("length", 1, database.getNbItems());
        BoolVar[] x = model.boolVarArray("x", database.getNbItems());
        model.sum(x, "=", length).post();
        model.post(new Constraint("Cover Size", new CoverSize(database, freq, x)));
        model.post(new Constraint("Cover Closure", new CoverClosure(database, x)));
        
        Overlap overlap = new Overlap(database, x, Tmax, theta, k, parallel);
        model.post(new Constraint("Overlap", overlap));
        Solver solver = model.getSolver();
        solver.plugMonitor(overlap);
        
        //DataSet dataset = new DataSet(dataPath);
        solver.setSearch(Search.intVarSearch(
                //new InputOrder<>(model),
                new MinCov(model, database),
                new IntDomainMax(),
                x
        ));
        
        while (solver.solve());
        //solver.printStatistics();
        itemsets = overlap.getItemsetsHistory();
        covers = overlap.getCoversHistory();
        System.out.println(itemsets.size());
        for (int i = 0; i < itemsets.size(); i++) {
            int[] itemset = Arrays.stream(itemsets.get(i))
                    .map(j -> database.getItems()[j])
                    .toArray();
            System.out.println(Arrays.toString(itemset) + ", cover=" + covers.get(i));
        }
        //System.out.println(solver.getSolutionCount());
        //write the results
        FilesResults(solver, itemsets, covers);
        
        argparam = args;
    }
}
