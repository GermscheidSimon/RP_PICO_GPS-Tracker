import rpConnectZero

def main():
    try:
        _rpPico_COM = rpConnectZero.rpConnectZero()
        _rpPico_COM.RX_data()
        data = _rpPico_COM.handshake.data
        print('great ')
        print(data)
    except:
        print('R2D2 Scream')
    finally:
        print('in theroy this is where I turn off')

if __name__ == "__main__":
    main()