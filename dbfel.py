import argparse
import panel.panel
import scope.scope

def main():
    desc = ''
    parser = argparse.ArgumentParser(description = desc)
    args = parser.parse_args()
    
    panel.panel.start_bokeh_server()
    
if __name__ == '__main__':
    main()
