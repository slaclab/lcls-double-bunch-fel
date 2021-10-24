import pulse.multipulse
import panel.panel

def main():
    multipulse = pulse.multipulse.Multipulse()
    thepanel = panel.panel.Panel(multipulse)
    
    thepanel.start()
    
if __name__ == '__main__':
    main()
