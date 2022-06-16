# KPMG_tax_documents
- Type of challenge: Learning
- Duration: `2 weeks`
- Deadline : `15/06/2022 04:30 PM`
- Presentations : `16/06/2022 01:30 PM`
- Team challenge: Group project
## Mission objectives

- Scrape legal content
- Use Natural Language Processing to analyze text
- Classify tax-related documents based on their content

## The Mission

For helping their customers, a tax department is constantly looking for law changes regarding tax matters in Belgium. To that purpose some members from the team spend up to 2 hours per day reading the [National Gazette](http://www.ejustice.just.fgov.be/cgi/welcome.pl) to look for tax law changes and to report them in an Excel file.

But as you know...time is money ! That's why the company would like to improve the process by automating a part of this job.

They have hired us to work on a NLP-based prototype for automating their task. They asked us to create a tool which scrapes the National Gazette and extracts the content which is relevant to them (*i.e* tax-related content). This content should be delivered in an Excel file similar to the files they are currently working on.

The customer expects us to be creative and let us to choose the method and to design the approach. We can use keyword-based approaches as well as neural models. Feel free to think out-of-the box in order to provide the most original and the most efficient solution.

## The Solution

According to the links and the desired [website](http://www.ejustice.just.fgov.be/cgi/welcome.pl), we scraped the texts and saved them in an Excel file.

For simplicity, we did some preprocessing.

Using Burt's model, we summarized the text and saved it in an Excel file.

The next step is to show you how to use scikit-learn to extract keywords from documents using TF-IDF.

Create an app that takes as input a text and returns the summury of text, the keywords and score how related the text to the taxes.

## Installation

- [numpy](https://numpy.org/)

- [pandas](https://pandas.pydata.org/)

- [sklearn](https://scikit-learn.org/stable/install.html)

## Usage

All notebooks are in the notebooks folder


## Contributors

- #### [Mahboubeh Faghih Mohammadi](https://github.com/mahboubehfaghih)
- #### [Malika Obkiche](https://github.com/obkiche)
- #### [Kristof Vandewynckel](https://github.com/KristofVandewynckel)

