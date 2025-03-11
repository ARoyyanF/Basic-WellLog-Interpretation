
def normalise(curve, ref_low, ref_high, well_low, well_high):
    return ref_low + ((ref_high - ref_low) * ((curve - well_low) / (well_high - well_low)))

def normalise_log(df, key_well, log):
    for i in log:
        df['05_PERC'] = df['WELL'].map(df.groupby('WELL')[i].quantile(0.05))
        df['95_PERC'] = df['WELL'].map(df.groupby('WELL')[i].quantile(0.95))
        key_well_low = df.groupby('WELL')[i].quantile(0.05)[key_well]
        key_well_high = df.groupby('WELL')[i].quantile(0.95)[key_well]
        list_norm = df.apply(lambda x: normalise(x[i], key_well_low, key_well_high, x['05_PERC'], x['95_PERC']), axis=1)
        df = df.drop([i, '05_PERC', '95_PERC'], axis=1)
        df[i] = list_norm

    return df