import argparse
import csv
import json
import io

import zstandard as zstd

CSV_FIELDS = ['subreddit', 'id', 'author', 'score', 'created_utc', 'body']

def convert(src: str, dst: str):
    with open(src, 'rb') as json_fh:
        dctx = zstd.ZstdDecompressor()
        stream_reader = dctx.stream_reader(json_fh)
        text_stream = io.TextIOWrapper(stream_reader, encoding='utf-8')

        with open(dst, 'w') as csv_fh:
            csv_writer = csv.DictWriter(
                csv_fh, fieldnames=CSV_FIELDS,
                delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL
            )
            for line in text_stream:
                data = json.loads(line)
                data_subset = {k: data[k] for k in data.keys() & {*CSV_FIELDS}}
                csv_writer.writerow(data_subset)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('src')
    parser.add_argument('dst')

    args = parser.parse_args()

    convert(src=args.src, dst=args.dst)
