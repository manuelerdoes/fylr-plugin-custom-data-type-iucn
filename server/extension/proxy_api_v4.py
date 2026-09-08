# coding=utf8

# API extension of custom-data-type-iucn. It forwards a request from the
# webfrontend to the IUCN API and answers with the JSON response. The API
# token is read from the base config and never leaves the server.

import json
import sys
import time
import urllib.error
import urllib.request

PLUGIN = 'custom-data-type-iucn'


def error(line: str) -> None:
    sys.stderr.write(line)
    exit(1)


def parse_api_settings(api_settings: dict) -> tuple[str, str]:

    def parse(key: str) -> str:
        value = api_settings[key]
        if not isinstance(value, str):
            raise Exception(f'expected {key} as string')
        value = value.strip()
        if value == '':
            raise Exception(f'expected {key} as non-empty string')
        return value

    return parse('api_url'), parse('api_token')


def perform_get_request(api_url: str, api_path: str, api_token: str) -> dict:
    # seconds to wait on consecutive 429 answers. longer waits would exceed the extension timeout
    retry_waits = [5, 10]
    attempt = 0

    request = urllib.request.Request(
        url=f'{api_url}/{api_path}',
        headers={
            'Authorization': api_token,
        },
    )

    while True:
        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            # when a search finds no result, the API v4 answers with 404
            if e.code == 404:
                return {}
            # rate limited — wait and retry up to len(retry_waits) times
            if e.code == 429 and attempt < len(retry_waits):
                time.sleep(retry_waits[attempt])
                attempt += 1
                continue
            raise Exception(f'HTTP status code: {e.code}, text: {e.read().decode("utf-8")}')

def main() -> None:
    if len(sys.argv) < 2:
        error('expect info.json as first parameter')

    # parse info.json parameter
    info_json = None
    try:
        info_json = json.loads(sys.argv[1])
    except Exception as e:
        error(f'could not parse info.json: {e}')

    # load query
    iucn_api_path = None
    try:
        iucn_query = info_json['request']['query']['iucn_query']
        if not isinstance(iucn_query, list):
            raise Exception('expected non empty array')
        if len(iucn_query) < 1:
            raise Exception('expected non empty array')
        iucn_api_path = iucn_query[0]
    except Exception as e:
        error(f'could not load query from info.json.request.query.iucn_query: {e}')

    # load config
    iucn_api_url = None
    iucn_api_token = None
    try:
        config = info_json['config']['plugin'][PLUGIN]['config']
        iucn_api_url, iucn_api_token = parse_api_settings(config['iucn_api_settings'])
    except Exception as e:
        error(f'could not parse iucn_api_settings: {e}')

    try:
        response = perform_get_request(
            api_url=iucn_api_url,
            api_token=iucn_api_token,
            api_path=iucn_api_path,
        )
        if not isinstance(response, dict):
            raise Exception('expected response as json dict')
        sys.stdout.write(json.dumps(response))
    except Exception as e:
        error(f'could not perform request to IUCN API {iucn_api_url}: {e}')


if __name__ == '__main__':
    main()
