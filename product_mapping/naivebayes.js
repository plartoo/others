// File reader: http://matthewmeye.rs/blog/post/html5-line-reader/
// http://blog.teamtreehouse.com/reading-files-using-the-html5-filereader-api
// https://www.html5rocks.com/en/tutorials/file/dndfiles/
// https://github.com/winkjs/wink-naive-bayes-text-classifier
// https://www.npmjs.com/package/wink-nlp-utils
//https://scotch.io/tutorials/getting-started-with-browserify
// Debug: node --inspect-brk naivebayes.js and launch Chrome about:inspect window; put a breaker and inspect
// or go CLI way: place 'debugger;' in the code; run node naivebayes.js and 'c' and 'repl' to inspect 


// var papa = require('papaparse');
//
// var data;
// papa.parse('test.csv', {//fs.readFile('test.csv'), {
//     header: true,
//     download: true,
//     dynamicTyping: true,
//     complete: function(results) {
//         data = results.data;
//         console.log("Finished:", results);
//     }
// })


// Load NLP utilities
var nlp = require('wink-nlp-utils');
var classifier = require('wink-naive-bayes-text-classifier');
var nbc = classifier();
// Configure preparation tasks
nbc.definePrepTasks( [ // REF: http://winkjs.org/wink-nlp-utils/#stringbong
  nlp.string.lowerCase,
  nlp.string.removeExtraSpaces,
  nlp.string.retainAlphaNums,
  // Simple tokenizer
  nlp.string.tokenize0,
  // Common Stop Words Remover
  nlp.tokens.removeWords,
  // Stemmer to obtain base word
  //nlp.tokens.stem
] );
// Configure behavior
nbc.defineConfig( { considerOnlyPresence: true, smoothingFactor: 0.5 } );

// Train!
// nbc.learn( 'I want to prepay my loan', 'prepay' );
// nbc.learn( 'I want to close my loan', 'prepay' );
// nbc.learn( 'I want to foreclose my loan', 'prepay' );
// nbc.learn( 'I would like to pay the loan balance', 'prepay' );
//
// nbc.learn( 'I would like to borrow money to buy a vehicle', 'autoloan' );
// nbc.learn( 'I need loan for car', 'autoloan' );
// nbc.learn( 'I need loan for a new vehicle', 'autoloan' );
// nbc.learn( 'I need loan for a new mobike', 'autoloan' );
// nbc.learn( 'I need money for a new car', 'autoloan' );

// Consolidate all the training!!
// nbc.consolidate();

// Start predicting...
// console.log( nbc.predict( 'I would like to borrow 50000 to buy a new Audi R8 in New York' ) );
// -> autoloan
// console.log( nbc.predict( 'I want to pay my car loan early' ) );


// Failed attempt to try this package: node-csv
// var csv = require('node-csv').createParser();
// var lines = 0;
// csv.each('./allmappings.csv').on('data', function(data){
//   lines++;
//   console.log(data);
// }).on('end', function(){
//   console.log(lines + ' lines parsed');
// })
// csv.parseFile('./allmappings.csv').on('data', function(data){
// csv.mapFile('./allmappings.csv', function(err, data){
//     console.log(data);
// })



var fs = require('fs');
var csv = require('fast-csv'); // REF: https://www.npmjs.com/package/fast-csv
var stream = fs.createReadStream('allmappings.csv');
csv
.fromStream(stream, {headers : true})
.on('data', function(data){
  // console.log(data.GM_COUNTRY_NAME);
  var str = data.GM_ADVERTISER_NAME + data.GM_SECTOR_NAME
      + data.GM_SUBSECTOR_NAME + data.GM_CATEGORY_NAME
      + data.GM_BRAND_NAME + data.GM_PRODUCT_NAME;
  nbc.learn(str,data.CP_SUBCATEGORY_NAME);
})
.on('end', function(data){
  nbc.consolidate();
  //debugger; // REF: https://blog.risingstack.com/how-to-debug-nodej-js-with-the-best-tools-available/
  console.log(nbc.predict('Norelco : Shaving Products'));
  console.log(nbc.predict('Norelco Series 8000 : Electric Shaver Men'));
    console.log('read finished');
});


// // REF: https://www.joyofdata.de/blog/parsing-local-csv-file-with-javascript-papa-parse/
// // http://archive.is/ySSC8
// document.getElementById('response1').innerHTML = nbc.predict( 'I would like to borrow 50000 to buy a new Audi R8 in New York' );
// document.getElementById('response2').innerHTML = nbc.predict( 'I want to pay my car loan early' );
// var data;
// function handleFileSelect(evt) {
//     var file = evt.target.files[0];
//     Papa.parse(file, {
//         header: true,
//         dynamicTyping: true,
//         complete: function(results) {
//             data = results;
//             console.log(data);
//             console.log('hahha');
//             console.log(nbc.predict( 'I would like to borrow 50000 to buy a new Audi R8 in New York' ));
//         }
//     });
// }
//
// $(document).ready(function(){
//     $("#csv-file").change(handleFileSelect);
// });
