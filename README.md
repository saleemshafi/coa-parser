# COA Zoning Info scraper

This repo is a set of Python scripts attempting to automate data mining of the City of Austing zoning information.  Unfortunately, the city only publishes this information as meeting minutes in PDF format.  The format and structure of the document is not consistent over time, making the extraction of data really difficult, so this wasn't as successful as I had hoped.

The contents are divided into three main pieces:

1. Downloading all of the City Council meeting minutes at https://www.austintexas.gov/department/city-council/archive/city_council_meeting_archives.htm
2. Downloading all of the Zoning meeting minutes at https://www.austintexas.gov/cityclerk/boards_commissions/meetings/
3. Trying to extract the zoning meeting minutes data, specifically the rezoning items and put them in CSV format.


## Downloading city council meeting minutes

This work is covered by the code in `coa_scraper`.  This uses the Scrapy framework and most of the meaningful logic is in `coa_scraper/coa_scraper/spiders/ACCMeetingSpider.py`.

From the `coa_scraper/coa_scraper` folder, execute this line:
```
scrapy runspider spiders/ACCMeetingSpider.py
```

There are a ton of files and this takes a while, but it should just be a one-time job.

Once downloaded, you can use pdf2text.py or pdf2text_py3.py to convert them to text and make them searchable. The first uses pdf2py and the second uses pdfminer to do the extraction.  I believe the latter produced more searchable results.

## Downloading zoning meeting minutes

This work is handled by download_minutes.csv and urls.txt.   I actually wrote this one first, before the city council minutes above, and since the number of pages was a lot smaller, I ended up manually recording the list of pages were the links were and downloading them fairly crudely.

The results are downloaded into a `./minutes` folder.

This could easily be redone in Scrapy as a separate spider, which would make it more useful for pulling the latest data.

## Extracting zoning data

The main file for this is `rezone.py`.  It uses the files downloaded into `./minutes` and attempts to extract data using regular expressions, and then output a CSV formatted representation of the key data for all rezoning items.

This solution uses Py2PDF to process the PDF and while the output of this is pretty sloppy with it's use of whitespace, it at least kept things in order.  pdfminer made more readable text, but it got confused by the tables and it ended up putting things out of order, which made it impossible to assign semantics to anything.

The overall structure is pretty simple, with the main work starting near the bottom and referencing the functions defined above.  The text processing is somewhat crude, but i'm hoping you can follow it.  The regular expressions may seem a bit odd, but most of that was trying to compensate for the whitespace craziness of Py2PDF.

I ran tests using a couple of different files trying to tweak the expressions to recognize the different sections while accounting for the inconsistencies in the text extraction, as well as the differences in the original formatting.  This was mildly successful, but some files still weren't processible.
