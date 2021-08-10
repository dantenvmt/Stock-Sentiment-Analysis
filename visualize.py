from wsb_plot import plot_scores
from wsb_scraper import scrape_for
import argparse
import os
import csv

def main():

    parser = argparse.ArgumentParser(
        description='Scrape and visualize sentiment and stock data.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--sub', type = str, default = 'wallstreetbets',
                        help = 'subreddit to scrape')
    parser.add_argument('--date', type = str, default = '30d',
                        help = 'how far back to scrape')
    parser.add_argument('--stock', type = str, default = 'amzn',
                        help = 'stock symbol to scrape')
    parser.add_argument('--limit', type = int, default = 100,
                        help = 'limit post to scrape')
    args = parser.parse_args()

    results = scrape_for('{}'.format(args.stock.lower()), args.limit, args.date, args.sub)
    results.to_csv('{0}_{1}_sentiment.csv'.format(args.stock, args.sub))
    plot_scores(results, '{} Sentiment and Stock Price'.format(args.stock), args.stock)

if __name__ == '__main__':
    main()