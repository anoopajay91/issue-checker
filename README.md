# issue-checker
To check issues with respect to a github project

To achieve the outcome, I have made use of github API.
Once user enters the URL, the url is sent to the server as a request parameter.

The server in turn sends the URL to https://api.github.com to receive information about the repository, and once the content is received, I'm finding out length of JSON content which would basically be the number of issues.

The solution could be improved if there was a provision in the API to just return count ( certain parameters ) instead
of the entire JSON which currently makes the response content heavy. Didn't have much time to explore the API. Initial idea was to scrape the website but that would have been tedious and a bad approach, comparatively this option seemed better.

The main code is present inside folder issuecounter/

check views.py - it contains functions that are used to display and compute
check templates/index.html - it contains html and jquery ajax function that calls and updates HTML

Link to the live website: http://issue-checker.herokuapp.com/

