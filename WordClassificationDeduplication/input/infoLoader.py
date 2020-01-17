import yaml
import os

last_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_account(path="\config\env.yaml"):
    try:
        f = open(last_path + path)
        rest = yaml.load(f, yaml.FullLoader)
        return rest
    except:
        raise ValueError()
    finally:
        f.close()


if __name__ == '__main__':
    print(get_account())
