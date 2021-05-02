/*
// Description:
// Google Apps Script to check keyword(s) in Reddit posts.
// When a keyword is found in the posts' title or text/body, 
// the script will send an email notification to designated 
// recipients. 
//
// To use this script, create a new Google Sheet (you can see the 
// screenshot named 'HowToSetUpTheGoogleSheetForTracking.png'
// instead of reading the paragraph below).
// In that sheet, create 'Subreddit', 'Keyword', 'LastPostName', 
// and 'EmailToNotify' columns (the column names can be different 
// as long as there are four column names in the first row of the 
// sheet). Then in row number 2 and onward, you would enter the 
// subreddit name (e.g., r/gamesale/new); the keyword to search 
// for (regular expression is okay such as Mega\s?Man to search 
// for any posts that mentions either 'Mega man' or 'megaman'); 
// and finally in column 'D', the email recipients of the 
// notifications (e.g., DrLight@gmail.com). As a specific example, 
// the Google Sheet will look something like this after you've 
// filled out the required input parameters:
// 
// Subreddit        Keyword        LastPostName        Email
// r/gamesale/new   Mega\s?Man                         DrLight@gmail.com
// r/gamedeals/new  donkey kong                        FunkyKong@gmail.com;DiddyKong@tropical.com
//
// Next, embed this script as a '*.gs' file in your Script Editor 
// of the above Google Sheet. Before running this script, your 
// Reddit username, password, client ID and client secret must 
// be added as the constant variables defined at the beginning 
// of this script (see a few lines below).
// 
// Finally, you can try to run this script in Apps Script's 
// editor or better, set up a trigger to run it periodically 
// (make sure to check Reddit's API limits as well as Google's 
// Apps Script API limits when deciding how often to run your 
// trigger!). Hope this script is useful when you need to 
// automate checking certain subreddits for keywords 
// every now and then (E.g., checking r/gamesale subreddit to 
// see if anyone is selling Mega Man 11 game.)
//
// Reddit API guide (how to obtain client ID and client secret):
// https://github.com/reddit-archive/reddit/wiki/OAuth2
// https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example
//
// Rate limits of Google Services:
// https://developers.google.com/apps-script/guides/services/quotas#current_quotas
*/

// UPDATE the constant values below with your
// Reddit username, password, client ID and client secret. 
// Client ID and client secret can be obtained by 
// following this guide (choose 'Script app' option as the 
// app type):
// https://github.com/reddit-archive/reddit/wiki/OAuth2
const REDDIT_USERNAME = '';
const REDDIT_PASSWORD = '';
const CLIENT_ID = '';
const CLIENT_SECRET = '';

// You can but don't need to update the constants below.
// LATEST_POST_NAMES_TO_REMEMBER is to remember up to X 
// number of latest posts we fetched so that when one of them 
// is deleted, we can still randomly pick one of them as 
// an input parameter for 'before' in the API request to
// fetch up to FETCH_POST_LIMIT number of latest posts starting 
// from that post onward. In other words, with the default
// values 3 and 100 respectively for these constant variables,, 
// we are remembering up to 3 latest post names; pick any of 
// them randomly for our next API query to fetch the posts that 
// are posted after one of these posts.
// If we only remember the ONE latest post name, we empirically 
// found that the API query does not return us any new post 
// if the post name we remember is deleted by the poster.
const NUM_OF_LATEST_POST_NAMES_TO_REMEMBER = 3; 
const FETCH_POST_LIMIT = 100; // number of posts to fetch per API read
const USER_AGENT = 'Subreddit Keyword Checker';

// You do NOT need to update these constant variables below.
const ACCESS_TOKEN_URL = 'https://www.reddit.com/api/v1/access_token';
const REDDIT_API_URL = 'https://oauth.reddit.com/';

function sendEmail(sheetName, emailAddressColRange, subject, message) {
  var emailAddressRange = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange(emailAddressColRange); 
  var emailAddresses = emailAddressRange.getValues();
  
  emailAddresses.forEach(function(emailAddress, i) {
    if (emailAddress[i] !== '') {
      console.log('Sending email(s) to: ' + emailAddress[i]);
      MailApp.sendEmail(emailAddress[i], subject, message);
    }
  });
}

function setCellValue(sheetName, cellValueInRangeFormat, value) {
    // Set value at the Google Sheet's cell.
    // REF: https://developers.google.com/sheets/api/guides/values
    SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange(cellValueInRangeFormat).setValue(value);
}

function getCellValue(sheetName, cellValueInRangeFormat) {
    // Retrieve value from the Google Sheet's cell.
    // REF: https://developers.google.com/sheets/api/guides/values
    return SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange(cellValueInRangeFormat).getValue();
}

function getAccessToken(userAgent){
  /*
  // REF 1: https://stackoverflow.com/questions/67341137/how-to-request-access-token-for-reddit-on-google-apps-script
  // REF 2: https://developers.google.com/apps-script/reference/url-fetch/url-fetch-app#getrequesturl,-params
  */
  var data = {
    'grant_type': 'password',
    'username': REDDIT_USERNAME,
    'password': REDDIT_PASSWORD
  };
  var options = {
    'method' : 'post',
    'payload' : data,
    'headers': {
      'User-Agent': userAgent,
      'Authorization':  'Basic ' + Utilities.base64Encode(`${CLIENT_ID}:${CLIENT_SECRET}`),
      },
  };

  var resp = UrlFetchApp.fetch(ACCESS_TOKEN_URL, options);
  return JSON.parse(resp.getContentText())['access_token'];
}

function extractUpToLastXPostNames(redditPosts, limit) {
  /*
  // Capture up to X (as defined by the input parameter 'limit')
  // number of post names in an array and return them.
  //
  // As to why we want to use this function, read the comment
  // near the top of this script file regarding this constant
  // variable: NUM_OF_LATEST_POST_NAMES_TO_REMEMBER.
  */
  var count = 0;
  var postNames = []

  redditPosts.forEach(function(post, i) {
    if (count < limit) {
      postNames.push(post['data']['name']);
      count++;
    }
  });

  return postNames;
}

function getLastPostName(postNameValuesCapturedInTheSheet){
    /* 
    // Get the latest post name that was read in the previous API call.
    // This will save us computation from re-reading/processing 
    // already-seen posts.
    //
    // If no post name was captured before (that is, the corresponding cell 
    // is empty), this function will return an empty string and the program 
    // will read 100 (defined as the variable 'FETCH_POST_LIMIT' above) 
    // latest posts from the corresponding subreddit.
    //
    // If some post names are captured, this function will randomly choose 
    // one of them to return so that the program can read any new posts 
    // after that particular post (to save re-processing them).
    */
    if (postNameValuesCapturedInTheSheet[0] !== ""){
      let postNames = JSON.parse(postNameValuesCapturedInTheSheet);
      let random = Math.floor(Math.random() * postNames.length);
      return postNames[random];
    }

    // return an empty string if we have not captured any post name previously
    return postNameValuesCapturedInTheSheet;
}

function extractMatchingPosts(posts, keyword) {
  /*
  // Scan for keyword(s) using REGEX in the title 
  // and the body of the Reddit posts.
  // Returns the posts that have keywords in them.
  */
  var matchingPosts = [];
  var regexPattern = new RegExp(keyword, 'i');

  posts.forEach(function(post, i) { 
    var postTitle = post['data']['title'];
    var postText = post['data']['selftext'];
    var postUrl = post['data']['url'];
    var matchResult = (postTitle + postText).match(regexPattern);

    if (matchResult !== null){
      // keyword match found in the post title and/or text.
      matchingPosts.push({
        '_title': postTitle,
        'post_url': postUrl
      })
    }
  });
  return matchingPosts;
}

function main() { 
  var accessToken = getAccessToken(USER_AGENT);

  var sheetNames = ['Sheet1'];
  var subredditRange = 'A2:A';
  var keywordRange = 'B2:B';
  var latestPostNameRange = 'C2:C';
  var emailAddressColLetter = 'D';
  // Cells which store subreddit and keyword info starts at index = 2
  var rowIndexOffset = 2; 

  sheetNames.forEach(function(sheetName) {
    // Instead of iterating the whole range (e.g., 'A2:A'),
    // we'll find the last row in the sheet and only 
    // iterate up until  that row to save computation.
    var lastRow = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getDataRange().getLastRow();

    // Get subreddits to track
    var subreddits = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange(subredditRange + lastRow).getValues();

    // Get keywords to track
    var keywords = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange(keywordRange + lastRow).getValues();

    /*
    // Get lastPostName that was read in the previous API call.
    // This will save us computation from re-reading/processing 
    // already-seen posts.
    //
    // If no post was read before, the program reads 100 (defined 
    // as the variable 'FETCH_POST_LIMIT' above) latest posts on the 
    // corresponding subreddit and store it in the corresponding 
    // cell under the latestPostNameRange column.
    */
    var lastPostNames = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange(latestPostNameRange + lastRow).getValues();

    subreddits.forEach(function(subreddit, i) {
      var keyword = keywords[i];
      var lastPostName = getLastPostName(lastPostNames[i]);

      /*
      // Unfortunately, Google Apps Script doesn't seem to support URL()
      // so we have to create the resourceUrl in an ugly way.
      // var resourceUrl = new URL(apiUrl + subreddit);
      // resourceUrl.searchParams.set('limit', postLimit);
      // resourceUrl.searchParams.set('before', lastPostName);
      */
      var resourceUrl = REDDIT_API_URL + subreddit + '?limit=' + FETCH_POST_LIMIT + '&before=' + lastPostName;
      var options = {
        'method' : 'get',
        'headers': {
          'User-Agent': USER_AGENT,
          'Authorization':  'bearer ' + accessToken,
          },
      };

      // console.log('Fetching URL: ' + resourceUrl.toString());
      // console.log('with options: ' + JSON.stringify(options));
      // console.log('For subreddit: ' + subreddit + ' and keyword: ' + keyword);
      var response = UrlFetchApp.fetch(resourceUrl.toString(), options);
      var redditPosts = JSON.parse(response.getContentText())['data']['children'];

      if (redditPosts.length >= NUM_OF_LATEST_POST_NAMES_TO_REMEMBER) {
        // Reddit API returns the most recent posts in a subreddit as the first child
        // We will capture/remember up to X number of them for future reads.
        let latestPostNames = extractUpToLastXPostNames(redditPosts, NUM_OF_LATEST_POST_NAMES_TO_REMEMBER);

        setCellValue(
          sheetName, 
          latestPostNameRange + (i + rowIndexOffset), // e.g., 'C2:C2'
          JSON.stringify(latestPostNames));
      }

      if (redditPosts.length > 0) {
        var matchingPosts = extractMatchingPosts(redditPosts, keyword);
        if (matchingPosts.length > 0) {
          sendEmail(
            sheetName,
            emailAddressColLetter + (i + rowIndexOffset) + ':' + emailAddressColLetter + (i + rowIndexOffset), // e.g., 'D3:D3'
            'Alert for "' + keyword + '" on subreddit "' + subreddit + '"', 
            JSON.stringify(matchingPosts, null, 4)
            );
        }
        else {
          console.log(
            'No matching post found in our last fetch for keyword: "' + 
            keyword + '" in subreddit: "' + subreddit + '"');
        }
      }
      else {
        console.log(
          'Nothing new posted since our last fetch for keyword: "' + 
          keyword + '" in subreddit: "' + subreddit + '"');
      }
    }); // end of subreddits.forEach
  }); // end of sheetNames.forEach
}
