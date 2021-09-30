import argparse
import panel.panel

def main():
    desc = ''
    parser = argparse.ArgumentParser(description = desc)
    args = parser.parse_args()
    
    panel.panel.show_panel()

if __name__ == "__main__":
    main()
