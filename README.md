# DCA Detect
I made a webscraper that would email me an HTML table with any updates to a case that affected my family that had been appealed to the 2nd District Court of Appeals in Florida. This script is very useful in that you can just set it up with cron or a systemd timer and it'll keep you apprised of the case instead of having to check yourself. This can be run on a headless machine.

## Setting up
Make sure to have an email account setup for the script to notify you from, check the comments in the file on which exact lines to edit. On the bottom it will have a function call to the check\_diff function which will check the file 2dca\_lastchk.txt for a date (the nickname is configurable). It will check if any of the data is greater than that date and then make the table, if the table is not empty it will call send\_email and then reformat it into a cleaner HTML table and send the email to you.

This will work with gmail if you enable App Passwords on the security dashboard of whatever account you want the notification coming *from* but Google will send you periodic emails complaining your account isn't as secure since someone can access it with a static password. If I have a lot of free time one day I might add in OAuth2 support but I have decided to publish a basic SMTP based one for now.

You can also monitor multiple cases by copying the function call to check\_diff at the bottom, and changing the URL **and the nickname**, the nickname must be unique for each case because the script will associate it with that lastchk.txt file. Otherwise you'll either be getting emails about things that have been sent to you before, or even worse missing out on emails because another case was already updated.

From experience the case updates will come out exactly at 5 PM, so you can probably set it to check once or twice a day, be mindful that you could be causing extra load on the server, which may encourage the server administators to implement web scraping counter-measures.

*This script was made in loving memory of Jose Lopez.*
