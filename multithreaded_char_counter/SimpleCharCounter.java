/**
 * @author  Phyo Thiha
 * @version 3/7/2015
 * 
 * Counts the number of occurrence of each (ASCII) character
 * in the files using simple (single-threaded) approach and
 * prints out the table of character count.
 * <p>
 * This class can be used to verify the results from my other
 * multi-threaded implementation. In addition, it is also used
 * to measure and compare the time against the multi-threaded
 * version.
 * <p>
 * To compile and run:
 * $ javac SimpleCharCounter.java
 * $ java SimpleCharCounter [pathToFolderWithTextFiles]
 * 
 * For example,
 * $ java SimpleCharCounter ./test
 * 
 * Note: For testing, I've provided the folder named "/test" 
 * which includes 100 files of different size, each of which 
 * contains randomly generated ASCII characters.
 */

import java.io.*;
import java.util.*;

public class SimpleCharCounter {
    private static Hashtable<Character, Integer> freqTable = 
            new Hashtable<Character, Integer>();
    private static File[] filenames = null;

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
     * Counts the characters by their occurrence and stores them
     * in the static variable, 'freqTable', of this class, which
     * which is the character count table.
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
            //System.out.println("Read: " + ch);
            if(!isExcluded(ch)) {
                if (freqTable.containsKey(ch)){
                    freqTable.put(ch, freqTable.get(ch)+1);
                }else{
                    freqTable.put(ch, 1);
                }
            }
        }
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
     * Shows user how to run the program
     */
    private static void printCorrectUsage(){
        System.out.println("\nIncorrect usage. Please try:");
        System.out.println("$ java SimpleCharCounter <pathToFolderWithFiles>\n");
        System.out.println("For example,\n$ java SimpleCharCounter ./test");
    }
    
    /**
     * Prepares the list of files inside a given folder to be processed.
     * 
     * @param   folder              folder that contains text files
     *                              to be processed
     * @throws  SecurityException   if read access to folder is denied
     */
    public static void loadFileNames(File folder) throws SecurityException{
        filenames  = folder.listFiles();
    }
    
    /**
     * Iterates through files loaded in the 'filenames' array and 
     * process them individually. Allows a boolean flag that, when 
     * set to <code>true</code>, would print out the final character
     * count table.
     * 
     * @param   verbose             boolean flag to determine if this
     *                              method should print the character
     *                              count table after processing.
     * @throws  IOException         if the file pathname is <code>null</code>
     * @throws  SecurityException   if read access to a file is denied
     */
    public static void countChars(boolean verbose) 
            throws IOException, SecurityException{
        for (int i = 0; i < filenames.length; i++){
            if (filenames[i].isFile()){
                //System.out.println("Processing file: " + filenames[i].getPath());
                processFile(new File(filenames[i].getPath()));
            }
        }
        
        if (verbose){
            printCharCountTable();
        }
    }

    public static void main(String[] args) throws Exception{
        long startTime = 0;
        long stopTime = 0;
        
        if (args.length != 1){
            printCorrectUsage();
            System.exit(0);
        }else{
            startTime = System.nanoTime();
            loadFileNames(new File(args[0]));
            countChars(false);  // start counting characters with verbose=false
            stopTime = System.nanoTime();
        }

        System.out.println("Processing files in folder: " + args[0]);
        System.out.println("SimpleCharCounter: Printing character count table...");
        printCharCountTable();
        System.out.println("SimpleCharCounter successfully completed!");
        System.out.println("Time taken: " + (stopTime - startTime) 
                + " nanoseconds.\n====\n");
    }
}
