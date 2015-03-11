/**
 * @author  Phyo Thiha
 * @version 3/7/2015
 * 
 * Runs simple and multi-threaded character counting programs
 * ten times each to calculate the average amount of time 
 * each approach takes. Prints out the average time taken
 * for each approach to the terminal (stdout).
 * <p>
 * In running the multi-threaded version, the program 
 * automatically tries running with 1, 2, 4, 8, 16, 64 threads 
 * to calculate the average performance over spawning more 
 * and more threads.
 * <p>
 * Since the goal of this program is to measure the time performance
 * it won't print out the character count table by default. 
 * For that, please run the corresponding classes (SimpleCharCounter 
 * or MultithreadCharCounter) individually or append a verbose flag
 * to the command to run this program as shown below.
 * <p>
 * To compile and run:
 * $ javac CharCountTest.java
 * $ java CharCountTest [pathToFolderWithTextFiles] [OptionalVerboseFlag]
 * 
 * For example,
 * $ java CharCountTest ./test
 * 
 * To run in verbose mode, please run:
 * $ java CharCountTest ./test 1
 * 
 * Note: For testing, I've provided the folder named "/book" 
 * which includes 100 files of different size, each of which 
 * contains randomly generated ASCII characters.
 */

import java.io.File;

public class CharCountTest {
    private static final int NUM_TEST = 10;  // average over NUM_TEST times
    private static final int MAX_THREAD = 64;  // max thread to spawn
    
    /**
     * Shows user how to run the program
     */
    private static void printCorrectUsage(){
        System.out.println("\nIncorrect usage. Please try:");
        System.out.println("$ java CharCountTest <pathToFolderWithFiles> "
                + "[Optional verbose flag=1]\n");
        System.out.println("For example,\n$ java CharCountTest ./book 1\n");
    }

    /**
     * @param   avg     average time taken over NUM_TEST iterations
     */
    private static void printAverageTime(long totalTimeTaken){
        System.out.println("Average time (in nanoseconds) over " + NUM_TEST + 
                " iterations: " + (totalTimeTaken /(long)NUM_TEST));
        System.out.println("==========\n");
    }
    
    /**
     * Runs SimpleCharCounter over NUM_TEST times and calculates,
     * and prints out average time taken.
     * 
     * @param   folderName      the folder where text files exist
     * @param   verbose         if <code>true</code>, prints character
     *                          count table after every test iteration
     * @throws  Exception       catches any exception that might be 
     *                          thrown by classes being used
     */
    private static void testSimpleCharCount(String folderName, boolean verbose) 
            throws Exception{
        SimpleCharCounter simpleCounter = new SimpleCharCounter();

        long sum = 0;
        for (int i = 0; i < NUM_TEST; i++){
            long startTime = System.nanoTime(); // Or System.currentTimeMillis();
            
            simpleCounter.loadFileNames(new File(folderName));
            simpleCounter.countChars(verbose);
            
            long timeTaken = System.nanoTime() - startTime;
            sum += timeTaken;
            System.out.println("SimpleCharCount test #" + (i+1) 
                    + " takes " + timeTaken + " nanoseconds.");
        }
        printAverageTime(sum);
    }
    
    /**
     * Runs MultiThreadCharCounter over NUM_TEST times with various
     * number of threads (1, 2, 4, 8, 16, 32 and 64) and prints
     * the average time taken.
     * 
     * @param   folderName      the folder where text files exist
     * @throws  Exception       catches any exception that might be 
     *                          thrown by classes being used
     */
    private static void testMultiThreadCharCount(String folderName)
            throws Exception{
        MultiThreadCharCounter mCounter = new MultiThreadCharCounter();
        
        // spawns 1, 2, 4, 8, 16, 32 and 64 threads
        for (int j = 1; j <= MAX_THREAD; j = j*2){
            long sum = 0;
            
            for (int i = 0; i < NUM_TEST; i++){
            
                long startTime = System.nanoTime();

                mCounter.spawnThreads(folderName, j);

                long timeTaken = System.nanoTime() - startTime;
                sum += timeTaken;
                System.out.println("MultiThreadCharCount test #" + (i+1) 
                        + " with " + j + " threads takes " + timeTaken 
                        + " nanoseconds.");
            }
            printAverageTime(sum);
        }
    }
    
    public static void main(String[] args) throws Exception{
        boolean verbose = false;
        
        if ((args.length < 1) || (args.length > 2)){
            printCorrectUsage();
            System.exit(0);
        }else if (args.length == 2){
            verbose = true;
        }
        
        System.out.println("\nTesting character counting programs begins...");
        System.out.println("Processing files in folder: " + args[0]);
        testSimpleCharCount(args[0], verbose);
        
        // let's ignore verbose for multithread because it's going to be too messy
        testMultiThreadCharCount(args[0]);
        
    }
}
