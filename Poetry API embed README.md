I added a Quill button on the Home page of my portfolio, which, when clicked, will access
this API of poems from "https://github.com/thundercomb/poetrydb/blob/master/README.md"
a free public poetry API. The API is called using JavaScript's built-in fetch() function
with a GET request to the endpoint https://poetrydb.org/random/1, which returns a random poem.
The API returns data in JSON format containing a poem with properties including "title",
"author", and "lines". The response is then parsed using. json() and the poem is inserted 
into the HTML as a pop-up.

This code to call the API was created entirely using Claude and was mostly created through this prompt:

Use the following website for the Poem API:

https://github.com/thundercomb/poetrydb/blob/master/README.md

Can you create code that when I click on a small quill button on the bottom right corner of an HTML page,
a pop up is generated that shows the Poem of the day with a background that looks like a medieval parchment
with the Title of the Poem on the top center, then the "By: " {Author Name} and then the full poem

And then to leave the pop-up there should be an x out button:
