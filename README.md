# issue-checker
To check issues with respect to a github project

To achieve the outcome, I have made use of github API.
Requests are being sent to https://api.github.com and once the content is received, I'm finding out length of JSON content,
which would basically be the number of issues.

The solution could be improved, if there was a provision in the API to just return count ( certain parameters ) instead
of the entire JSON which currently makes the response content heavy.

