'''
Created on Oct 10, 2014

@author: Jason
'''
import numpy as np

def price_min_limit(historicaldata, min_price):
    events = (historicaldata.unnormalized_data['actual_close']).copy()*np.NaN
    event_index = np.zeros(historicaldata.unnormalized_data['actual_close'].shape, dtype=np.bool8)
    event_index[1::,:] = (historicaldata.unnormalized_data['actual_close'].iloc[0:-1,:].values >= min_price) & \
                         (historicaldata.unnormalized_data['actual_close'].iloc[1::,:].values   < min_price)
    events = events.where(~event_index,1)
    return events