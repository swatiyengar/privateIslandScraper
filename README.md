# privateIslandScraper Autoscraper
 Private island sales scraper

Don't we all day dream about having "Bezos" money? Or at minimum, "David Schwimmer" money? I certainly do...and maybe I'd throw a few 'pennies' down on a private island. 

Using GitHub Actions and Python, this repo automatically scrapes the content of [Private Islands, Inc](https://www.privateislandsonline.com/search?availability=sale). New listings will be appended to island_scrape file as an archive, while a new file full of current listings will created each week. 

Files in repo:
- scrape.py: python scraping script
- island_scrape.csv: scraped island database, updated and appended weekly
- island_scrape_weekly.csv: current week's listings only of the scraped island database; pricing data cleaned for further viz
- Private Island for Sale.ipynb: jupyter notebook explaining process
- .github/workflows: yaml file for automation
