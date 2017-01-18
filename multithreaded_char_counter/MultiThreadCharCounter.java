/**
 * @author  Phyo Thiha
 * @version 3/7/2015
 * 
 * Counts the number of occurrence of each (ASCII) character
 * in the files using multi-threaded approach and prints out
 * the table of character count.
 * <p>
 * Allows creation of up to 64 threads at one time and 
 * give each thread a tasks to read and count characters
 * from one file, until all the files are processed.
 * <p>
 * To compile and run:
 * $ javac MultiThreadCharCounter.java
 * $ java MultiThreadCharCounter [pathToFolderWithTextFiles] [threadCount]
 * 
 * For example,
 * $ java MultiThreadCharCounter ./test 32
 * <p>
 * Note: For testing, I provided the folder named "/book" 
 * which includes 100 files of different size, each of which 
 * contains randomly generated ASCII characters.
 */

import java.io.*;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public class MultiThreadCharCounter implements Runnable{
    
    /**
     * Chose ConcurrentHashMap over Hashtable because:
     * http://stackoverflow.com/questions/11710782/java-hashtable-concurrency
     */
    private static ConcurrentHashMap<Character, AtomicInteger> freqTable = 
            new ConcurrentHashMap<Character, AtomicInteger>();
    private static File[] filenames = null;
    private static int filePosition = 0;
    
    private static final int MAX_THREAD = 64;   // max allowed thread number
    
    /**
     * Checks if a character is space, tab, newline or carriage
     * return. We will exclude them from counting and printing
     * because they don't show up well when printing to the terminal.
     * If we want to include them in the count, we can simply not
     * use this method.
     * 
     * @param   ch          character we want to check
     * @return  Boolean     <code>true</code> if the character is a 
     *                      space, tab, newline or carriage return.
     *                      <code>false</code> otherwise
     */
    private static boolean isExcluded(char ch){
        return ((ch == ' ') || ( ch == '\n' ) || ( ch == '\r' )
                || ( ch == '\t' ));
    }

    /**
     * If the character is already in the table, increment its
     * count in a thread-safe way. If not, set it to AtomicInteger
     * value of 1.
     * 
     * @param   ch          character we want to update in the table
     */
    private static synchronized void incrementCharCount(char ch) {
        if (!freqTable.containsKey(ch)) {
            freqTable.put(ch, new AtomicInteger(1));
        }
        else { // this is different from Hashtable approach due to AtomicInteger
            freqTable.get(ch).incrementAndGet();
        }
    }

    /**
     * Counts the characters by their occurrence and stores them
     * in the static variable, 'freqTable', of this class, which
     * which is the character count table. Here, we use incrementCharCount
     * method, which is synchronized to ensure thread-safe update of 
     * the character count table.
     * 
     * @param   reader                  instance of the BufferedReader
     *                                  associated with a file input stream
     *                                  that we are interested in counting
     * @throws  IOException             if BufferedReader fails to read
     * @throws  NullPointerException    if key for Hashtable is null
     */
    private static void countCharacters(BufferedReader reader) 
            throws IOException, NullPointerException{
        int r = 0;
        while ((r = reader.read()) != -1){
            char ch = (char)r;
            //System.out.println("Read charcter: " + ch);
            if(!isExcluded(ch)) {
                incrementCharCount(ch);
            }
        }
    }

    /**
     * Returns the File object that is needed by 'processFile'
     * method. This must be synchronized so that no more than
     * one thread at a time can manipulate this array.
     * 
     * @return  File        the file object to process by the 
     *                      caller thread
     */
    private static synchronized File getNextFile(){
        if (filePosition == filenames.length){
            return null;
        }
        return filenames[filePosition++];
    }
    
    /**
     * Creates a BufferedReader instance from the File instance
     * provided and calls the main method of this class to start
     * counting characters in that specific file.
     * 
     * @param   file            instance of the file we want to read
     *                          and count the characters from
     * @throws  IOException     if BufferedReader and other StreamReader
     *                          instances fail
     */
    private static void processFile(File file) throws IOException{
        try(
            InputStream in = new FileInputStream(file);
            Reader reader = new InputStreamReader(in);
            BufferedReader buffer = new BufferedReader(reader)){
                countCharacters(buffer);
            }
    }
    
    /**
     * Retrieves next file and process it. Overrides the method 'run'
     * from Runnable interface. Not very sure about what to do with
     * exception caught here other than printing the stack trace.
     */
    @Override
    public void run(){
        while (true){
            File file = getNextFile();
            if (file == null){
                break;
            }
            
            try{
                processFile(file);
            }
            catch (Exception e){
                e.printStackTrace();
            }
        }
    }

    /**
     * Prepares the list of files inside a given folder to be processed.
     * 
     * @param   folderName          name of the folder that contains text files
     *                              to be processed
     * @throws  SecurityException   if read access to folder is denied
     */
    public static void loadFileNames(String folderName) throws SecurityException{
        filenames  = new File(folderName).listFiles();
    }

    /**
     * Spawns threads and starts processing the files until the file
     * array has nothing left (see 'run'). After that terminates the threads.
     * 
     * @param   folderName      path name in String of the folder
     * @param   threadNum       number of threads to spawn
     * @throws  Exception       catch all kinds of exception that can be thrown
     */
    public void spawnThreads(String folderName, int threadNum) throws Exception{
        // Step 1: load the files into arry and set the array position to beginning
        synchronized(this){
            loadFileNames(folderName);
            filePosition = 0;
        }

        // Step 2: populate array of threads with desired num of threads and start
        ArrayList<Thread> threads = new ArrayList<Thread>();
        for (int i = 0; i < threadNum; i++){
            //System.out.println("Thread# " + i);
            Thread t = new Thread(this);
            threads.add(t);
            
            t.start();      // this will in turn calls 'run'
        }

        // Step 3: when threads are done, we'll get here and join them
        for (Thread t : threads){
            t.join();
        }
    }

    /**
     * Prints the character count table using the stored information
     * in the static variable 'freqTable'. This is used before
     * exiting the main() of the program for visually inspecting
     * and verifying the correctness of the program.
     */
    private static void printCharCountTable(){
        Enumeration en = freqTable.keys();
        while (en.hasMoreElements()){
            char key = (char) en.nextElement();
            System.out.println( key + " => " + 
                    freqTable.get(key));
        }
    }

    /**
     * Shows user how to run the program.
     */
    private static void printCorrectUsage(){
        System.out.println("\nIncorrect usage. Please try:");
        System.out.println("$ java MultiThreadCharCounter <pathToFolderWithFiles> <numOfThread>\n");
        System.out.println("For example,\n$ java MultiThreadCharCounter ./test 8");
    }

    /**
     * Parses the second argument of the command passed to extract
     * the number of threads that needs to be spawn for this process.
     * 
     * @param   numStr          number of threads in <code>String</code>
     * @return                  number of threads in <code>Integer</code>
     */
    private static int getThreadNum(String numStr) {
        int threadNum = Integer.parseInt(numStr);
        if ((threadNum < 1) || (threadNum > MAX_THREAD)){
            throw new IllegalArgumentException("Thread number allowed is "
                    + "between 1 and " + MAX_THREAD);
        }
        
        return threadNum;
    }
    
    public static void main(String[] args) throws Exception{
        long startTime = 0;
        long stopTime = 0;

        if (args.length < 2){
            printCorrectUsage();
            System.exit(0);
        }else{
            MultiThreadCharCounter charCounter = new MultiThreadCharCounter();
            startTime = System.nanoTime();
            charCounter.spawnThreads(args[0], getThreadNum(args[1]));
            stopTime = System.nanoTime();
        }

        System.out.println("Processing files in folder: " + args[0]);
        System.out.println("MultithreadCharCounter: Printing character count table...");
        printCharCountTable();
        System.out.println("MultithreadCharCounter with " 
                + " threads successfully completed!");
        System.out.println("Time taken: " + (stopTime - startTime) 
                + " nanoseconds.\n====\n");
    }
}
