/*
Description: This AppScript can be embedded in Google Sheet's
Script Editor and run periodically to keep track of stock
prices of interest. This script also allows the user to
set ceiling and floor prices to trigger email alerts
(e.g., to buy/sell stocks at certain prices).

Please see the screenshot included in this folder to
set up the columns in the Google Sheet as this script
expects price information in specific columns
(or feel free to adapt this script as a base do arrange
columns as you see fit).

Disclaimer: This code still needs to be refactored a bit
more. I created this AppScript to replace another pure
JavaScript code that I wrote a while ago (2-3 years ago?)
to keep track of my stocks. That JS code require the use
of a third-party API and web storage. Turns out, that JS code
not only requires a bit of maintenance (because of the use
of an external API) but the external API was no longer
supported by the data provider, so I decided to write this
quick-and-dirty AppScript which utilizes GoogleFinance to
still keep track of my stocks in 2020.

Usage: To use this script as it is, you must:
1) set up a Google Sheet with columns similar to what I've
shown in the attached screenshot 'LayoutOfColumnsToUseWithTheProvidedScript')
2) in the Google Sheet created above, embed this script by
navigating to the menu option => Tools > Script editor and
in the opened code editor, copy paste this code and save it
(e.g., as 'stockPriceAlert')
3) set up time-driven trigger for this embedded script
(e.g., 'stockPriceAlert') by following the instruction below:
[https://developers.google.com/apps-script/guides/triggers/installable]
4) modify the script as you see fit for your personal use
(e.g., update sheet name; update email message content; add
other interesting columns related to the stock data available
via Google Finance API)

Author: Phyo Thiha
Last Updated: February 3, 2020
 */


function _sendEmail(sheetName, emailAddressColRange, subject, message) {
    var emailAddressRange = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange(emailAddressColRange); //'lacheephyo@gmail.com';
    var emailAddresses = emailAddressRange.getValues();

    emailAddresses.forEach(function(emailAddress, i) {
        if (emailAddress[i]) {
            MailApp.sendEmail(emailAddress[i], subject, message);
        }
    });
}


function setCellValue(sheetName, cellValueInRangeFormat, value) {
    // REF: https://developers.google.com/sheets/api/guides/values
    // E.g., cellValueInRangeFormat => "J2:J2"
    // value => "12
    SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange(cellValueInRangeFormat).setValue(value);
}


function getCellValue(sheetName, cellValueInRangeFormat) {
    // REF: https://developers.google.com/sheets/api/guides/values
    // E.g., cellValueInRangeFormat => "J2:J2"
    return SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange(cellValueInRangeFormat).getValue();
}


function getLatestTimeEmailWasSent(sheetName, range) {
    return getCellValue(sheetName, range);
}


function isSameDate(dateTime, anotherDateTime) {
    return (dateTime.getFullYear() === anotherDateTime.getFullYear()) &&
        // getMonth is 0-indexed
        (dateTime.getMonth() === anotherDateTime.getMonth()) &&
        (dateTime.getDate() == anotherDateTime.getDate());
}


function getCellRangeForLastEmailSentAt(colAlphabeticalLetterForLastEmailSentTime, curArrayIndex, rowNumberAndValueArrayIndexOffset) {
    var curRowNum = curArrayIndex + rowNumberAndValueArrayIndexOffset;
    // E.g., returns "J5:J5" for curArrayIndex = 3 (meaning, if the value array's index is 3,
    // we add the offset, which is '2' for the tracking sheet, and return the cell value/range
    // to which we should write the timestamp at
    return colAlphabeticalLetterForLastEmailSentTime + curRowNum + ":" + colAlphabeticalLetterForLastEmailSentTime + curRowNum
}


// REF: Usage to call UI alert
// var ui = SpreadsheetApp.getUi();
// ui.alert("(Buy alert) Current price for stock: " + tickers[i] + " is =>" + curPrices[i] + " and is equal/lower than the ceiling price => " + buyPrices[i]);
function checkPrices() {
    // REF: if we want get all sheets and iterate, try this: function sheetnms() {return SpreadsheetApp.getActiveSpreadsheet().getSheets().map(function(x) {return x.getName();});}
    var sheetNames = ["Sheet1"]; // ToDo: feel free to give your sheet a custom name and enter that sheet name here
    var emailAddressColRange = 'O2:O';
    // Below (awkwardly-named) variable exist because when we get array from AppScript via getValues(),
    // the index starts at 0 but the ranges in our cells (with values that we care about) starts at 2.
    var rowNumberAndValueArrayIndexOffset = 2;
    var lastEmailSentAtColVal = 'N';

    sheetNames.forEach(function(sheetName) {

        var tickerRange = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange("A2:A");
        var tickers = tickerRange.getValues();

        var curPriceRange = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange("C2:C");
        var curPrices = curPriceRange.getValues();

        // Get in desired stock prices (to sell)
        var sellPricesRange = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange("K2:K");
        var sellPrices = sellPricesRange.getValues();

        // Get max desired stock prices (to buy)
        var buyPricesRange = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName).getRange("L2:L");
        var buyPrices = buyPricesRange.getValues();

        curPrices.forEach(function(curPrice, i) {
            var cellRangeOfLastEmailSentAt = getCellRangeForLastEmailSentAt(lastEmailSentAtColVal, i, rowNumberAndValueArrayIndexOffset);
            var lastEmailSentAt = getLatestTimeEmailWasSent(sheetName, cellRangeOfLastEmailSentAt);
            var curDateTime = new Date(Date.now());
            var boolSendEmail = false;

            if ((buyPrices[i]) && (tickers[i]) && (parseFloat(curPrices[i]) <= parseFloat(buyPrices[i]))) {
                var subject = 'Buy Alert: ' + tickers[i];
                var message = "(Buy alert) Current price for stock: " + tickers[i] + " is =>" + curPrices[i] + " and is equal/lower than the alert price => " + buyPrices[i];
                var boolSendEmail = true;
            } else if ((sellPrices[i]) && (tickers[i]) && (parseFloat(curPrices[i]) >= parseFloat(sellPrices[i]))) {
                var subject = 'Sell Alert: ' + tickers[i];
                var message = "(Sell alert) Current price for stock: " + tickers[i] + " is =>" + curPrices[i] + " and is equal/higher than the alert price => " + sellPrices[i];
                boolSendEmail = true;
            }

            // REF: new Date("Fri Feb 28 2020 21:32:03 GMT-0500 (Eastern Standard Time)") => Fri Feb 28 2020 21:32:03 GMT-0500 (Eastern Standard Time)
            // console.log(new Date(Date.now())); => Fri Feb 28 2020 21:32:03 GMT-0500 (Eastern Standard Time)
            // console.log(Date.now()); => 1582943469871
            if (boolSendEmail && ((lastEmailSentAt === "") || (!isSameDate(curDateTime, lastEmailSentAt)))) {
                _sendEmail(sheetName, emailAddressColRange, subject, message);
                setCellValue(sheetName, cellRangeOfLastEmailSentAt, new Date(Date.now()));
            }
        }); // end of curPrices iterator

    }); // end of sheetNames iterator

} // end of function checkPrices