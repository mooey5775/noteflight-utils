import argparse
import zlib
import base64
import requests
import re

BASE_URL = 'https://www.noteflight.com/score_content/'
SCORE_REGEX = r'<noteflightCompressed>(.*)<\/noteflightCompressed>'

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--score', required=True,
                    help="Score ID to fetch")
    args = vars(ap.parse_args())

    # for some reason, noteflight's scoreContentUri has some number
    # after the score ID. As far as I can tell, this is unneeded
    # and I don't understand why it's there
    req_url = f'{BASE_URL}{args["score"]}'
    
    resp = requests.get(url=req_url)

    if resp.status_code != 200:
        # oops, request failure
        raise RuntimeError(f"[ERROR] Request failed with status {resp.status_code}")

    score_matches = re.match(SCORE_REGEX, resp.text)

    if score_matches is None:
        raise ValueError(f"[ERROR] Invalid request response {resp.text}")

    compressed_score = base64.b64decode(score_matches.group(1))

    score = zlib.decompress(compressed_score, wbits=15)

    with open(f'{args["score"]}.xml', 'wb') as f:
        f.write(score)
