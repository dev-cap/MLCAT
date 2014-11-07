MailingListParser
=================
Java code to parse mailing lists conforming to Mailman format
====

This module is capable of parsing out the Mailing List conforming to Mailman Format and scrape the relevant data out of it. For this implementation, the sample mailing list is taken as "http://www.spinics.net/lists/alsa-devel/".

On running the code, four text files are generated. 
1. page_list.txt -- This parses out the list of all the subsequent webpages that correspond to a specific mailing list.
2. msgid_list.txt -- This parses out the list of the Message Identification Number of all the messages existing in the mailing list.
3. msg_info.txt -- This parses out the To, From, In-Reply_to and References from each of the messages in the mailing list.
4. to_cc_info.txt -- This sums up the number of recipients for each messsage.


The implementation is divided among the classes as follows:

(1) MainClass.java
It is responsible for calling the other classes. It has the main function in it.

(2) URLFirstPage.java
It writes all the Message Id's in the first web-page of the mailing list to msgid_list.txt. It also gives the link of the next web-page of mailing list to URLRestPages.

(3) URLRestPages.java
It has the functions write_pagelinks(), read_pagelinks(), get_all_msgid(String link).  The function write_pagelinks() takes the curent webpage and writes the address of subsequent web-page of Mailing List to page_list.txt. The function read_pagelinks(), when called by URLFirstPage.java reads the current web-page link and calls the function get_all_msgid(String link), so that all Message Id's in that page are written into msgid_list.txt.

After the execution of URLFirstPage.java and URLRestPages.java, we have the Message Id's of all the messages existing in the mailing list.

(4) MessageExtract.java
It reads each Message Id from msgid_list.txt and writes information about To, From, In-Reply_to and References in msg_info.txt. On tconsole, "Hello" is printed whenever the next page is fetched and "^" is printed when information about it is being extracted from that page.

It also calls functions in To_CC_Sum.java to give information about To and CC; so that the function (in class To_CC_Sum.java), for calculating the sum of recipients for the corresponding Message Id, can be called. 

(5) To_CC_Sum.java
It calculates the sum of all recipients for a corresponding Message Id and writes it into to_cc_info.txt.

Building
--------
javac -classpath ".:jsoup-1.7.3.jar" MainClass.java

Running
--------
The parser may be run in two modes, `1. extract_URL ` and `2. extract_URL_info`, covered here. The former parses out all the Message Id's while the latter parse out the information from each of them.

1. java -cp ".:jsoup-1.7.3.jar" MainClass extract_URL 

2. java -cp ".:jsoup-1.7.3.jar" MainClass extract_URL_info
