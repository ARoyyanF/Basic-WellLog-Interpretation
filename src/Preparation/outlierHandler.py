def nanHandler(data, handler):
    numeric_cols = data.select_dtypes(include=['number']).columns
    if handler == "mean":
        data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())
        save_name = "data_clean_mean.txt"
    elif handler == "median":
        data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())
        save_name = "data_clean_median.txt"
    elif handler == "zero":
        data[numeric_cols] = data[numeric_cols].fillna(0)
        save_name = "data_clean_zeros.txt"
    else :
        save_name = "data_clean_NaN.txt"
        data[numeric_cols] = data[numeric_cols].fillna(-999.25)
    return data, save_name

#Isolation forest model fitting
def outlierHandler(data, anomaly_inputs, model_IF):
    list_anomaly_scores = []
    list_anomaly = []
    # if data.isna().any().any() :
    #     return data
    for i in data['WELL'].unique():
        df_WELL = data[data['WELL'] == i]
        model_IF.fit(df_WELL[anomaly_inputs])
        df_WELL['anomaly_scores'] = model_IF.decision_function(df_WELL[anomaly_inputs])
        df_WELL['anomaly'] = model_IF.predict(df_WELL[anomaly_inputs])
        for j, k in zip(list(df_WELL['anomaly_scores']), list(df_WELL['anomaly'])):
            list_anomaly_scores.append(j)
            list_anomaly.append(k)

    data['anomaly_scores'] = list_anomaly_scores
    data['anomaly'] = list_anomaly

    return data

def anomalyInterpolation(anomaly_inputs, interpolate, handled_data):
    param = 'DEPT'
    for i in anomaly_inputs:
        for j in range(0, len(list(handled_data[i]))-1):
            if (list(handled_data[i])[j] == -999.25) & (interpolate[j] == 1):
                handled_data[i].iloc[j] = handled_data[i].iloc[j-1] + (handled_data[param].iloc[j] - handled_data[param].iloc[j-1])*(handled_data[i].iloc[j+1] - handled_data[i].iloc[j-1])/(handled_data[param].iloc[j+1] - handled_data[param].iloc[j-1])
            elif interpolate[j] == -1:
                if handled_data['WELL'].nunique() == 1:
                    handled_data[i].iloc[j] = handled_data[i].iloc[j+1] + (handled_data[param].iloc[j] - handled_data[param].iloc[j+1])*(handled_data[i].iloc[j+2] - handled_data[i].iloc[j+1])/(handled_data[param].iloc[j+2] - handled_data[param].iloc[j+1])
                else:
                    if handled_data['WELL'].iloc[j+1] == handled_data['WELL'].iloc[j]:
                        handled_data[i].iloc[j] = handled_data[i].iloc[j+1] + (handled_data[param].iloc[j] - handled_data[param].iloc[j+1])*(handled_data[i].iloc[j+2] - handled_data[i].iloc[j+1])/(handled_data[param].iloc[j+2] - handled_data[param].iloc[j+1])
                    elif handled_data['WELL'].iloc[j-1] == handled_data['WELL'].iloc[j]:
                        handled_data[i].iloc[j] = handled_data[i].iloc[j-2] + (handled_data[param].iloc[j] - handled_data[param].iloc[j-2])*(handled_data[i].iloc[j-1] - handled_data[i].iloc[j-2])/(handled_data[param].iloc[j-1] - handled_data[param].iloc[j-2])
    return handled_data

def anomalyMarker(handled_data):
    interpolate = []
    for well in handled_data['WELL'].unique():
        # Get data for current well
        well_data = handled_data[handled_data['WELL'] == well]
        anomaly_list = list(well_data.anomaly)

        for i in range(len(anomaly_list)):
            current_anomaly = anomaly_list[i]

            if current_anomaly == -1:
            # Check if it's first or last point
                if i == 0 or i == len(anomaly_list) - 1:
                # Needs extrapolation
                    interpolate.append(-1)
                else:
                # Check surrounding points
                    prev_anomaly = anomaly_list[i-1]
                    next_anomaly = anomaly_list[i+1]

                # If both surrounding points are 1, needs interpolation
                    if prev_anomaly == 1 and next_anomaly == 1:
                        interpolate.append(1)
                    else:
                    # No interpolation needed
                        interpolate.append(0)
            elif current_anomaly == 1:
            # No interpolation needed for normal points
                interpolate.append(0)
                
        return interpolate
