def SMA_analysis(close_data, period):
    '''
    parameter: close_data = closing price array (type: np.ndarray.float64)
    return	 : 1. signal
                  - within period  = False(Invalid)
                  - greater period = return True(above SMA) and False(below SMA)
               2. SMA
                  - moving average result
    '''
    data_len 		= len(close_data)
    SMA				= np.zeros(data_len)
    signal 			= np.zeros(data_len, dtype = bool)

    if data_len > period:
        SMA  			= talib.SMA(close_data, period).astype(np.float32)
        signal[period:] = close_data[period:] > SMA[period:]
        log.info('SMA: Complete')
        return (signal, SMA)
    else:
        log.error('SMA: Data length < 200 ')
        return (signal, SMA)