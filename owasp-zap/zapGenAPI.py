import yaml #pip install pyyaml
import json
import argparse

parser = argparse.ArgumentParser(description='Generates a new openAPI json file with server url specification given an existing openAPI json or yaml file')
parser.add_argument('-f','--file', type=str, metavar='', required=True, help='openAPI json or yaml file')
parser.add_argument('-u','--url', type=str, metavar='', required=True, help='url of server')
args = parser.parse_args()

def main():
    if args.file.lower().endswith('.json'):
        api_file = open(args.file, 'r+')
        json_data = json.load(api_file)
        json_data['servers'] = [{'url':args.url}]
        api_file.close()
        api_file = open('zap_openapi.json', 'w')
        json.dump(json_data, api_file, indent=2, sort_keys=True)
        api_file.close()
    elif args.file.lower().endswith('.yaml') or args.file.lower().endswith('.yml'):
        api_file = open(args.file, 'r+')
        yaml_data = yaml.safe_load(api_file)
        yaml_data['servers'] = [{'url':args.url}]
        api_file.close()
        api_file = open('zap_openapi.json', 'w')
        json.dump(yaml_data, api_file, indent=2, sort_keys=True)
        api_file.close()
    else:
        raise Exception('Not a yaml or json file')

    return

if __name__ == "__main__":
    main()