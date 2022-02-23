import awg.multipulse
import panel.panel

def main():
    multipulse = awg.multipulse.Multipulse()
    thepanel = panel.panel.Panel(multipulse)
    
    thepanel.start()
    
if __name__ == '__main__':
    main()
