import pulse.multipulse
import panel.panel

def main():
    multipulse = pulse.multipulse.Multipulse()
    controls = panel.panel.Controls(multipulse)
    
    controls.start()
    
if __name__ == '__main__':
    main()
